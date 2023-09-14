package camel;

import org.apache.camel.builder.RouteBuilder;
import org.springframework.stereotype.Component;
import org.apache.camel.model.dataformat.JsonLibrary;
import org.apache.camel.Exchange;

import org.apache.camel.component.mongodb.MongoDbConstants;
import com.mongodb.client.model.Filters;
import com.mongodb.BasicDBObject;
import org.bson.conversions.Bson;
import org.apache.camel.Expression;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

import org.apache.camel.ProducerTemplate;

import java.util.Map;
import java.util.ArrayList;
import java.util.List;
import java.util.LinkedHashMap;
import org.bson.types.ObjectId;
import org.bson.Document;

import java.util.Base64;
import org.springframework.beans.factory.annotation.Value;

@Component
public class MySpringBootRouter extends RouteBuilder {

    @Value("${edge.contributor.username}")
    private String edgeContributorUsername;

    @Value("${edge.contributor.password}")
    private String edgeContributorPassword;

    private String storedDateTime = "";

    @Override
    public void configure() {
        String edgeContributorAuthString = Base64.getEncoder().encodeToString((edgeContributorUsername + ":" + edgeContributorPassword).getBytes());

        from("timer:startTimer?delay=1&repeatCount=1").startupOrder(1)
            .process(exchange -> {
                storedDateTime =  LocalDateTime.now().format(DateTimeFormatter.ofPattern("dd/MM/yyyy HH:mm:ss"));
             });

        //store automatic generated data from the datasythesizer in the mongoDB
        from("timer://myTimer?period={{timer.period}}").startupOrder(2).routeId("storeAutoSynthesizedData")
            .process(exchange -> {
                exchange.setProperty("storedDateTime", storedDateTime);
            })
            .log("Stored DateTime: ${exchangeProperty.storedDateTime}")
            .setHeader(Exchange.HTTP_METHOD, constant("POST"))
            .setHeader(Exchange.CONTENT_TYPE, constant("application/json"))
            .setBody(simple("{\"start_time\":\"${exchangeProperty.storedDateTime}\"}"))
            .to("{{datasynthesizer.uri}}" + "/synthesise_data_auto_call/")
            .process(exchange -> {
                storedDateTime = LocalDateTime.parse(storedDateTime, DateTimeFormatter.ofPattern("dd/MM/yyyy HH:mm:ss"))
                    .plusHours(1)
                    .format(DateTimeFormatter.ofPattern("dd/MM/yyyy HH:mm:ss"));
            })
            .unmarshal().json(JsonLibrary.Jackson, Map.class)
            .to("mongodb:myDb?database={{spring.data.mongodb.database}}&collection={{mongodb.user.data.collection}}&operation=insert")
            .log("Data inserted successfully at ${date:now:dd/MM/yyyy HH:mm:ss}")
            .to("direct:predictHealthData");
        
        //get agreements of the edgenode
        from("jetty:http://0.0.0.0:8030/getAgreements").routeId("getAgreements")
            .setHeader(Exchange.HTTP_METHOD, constant("GET"))
            .setHeader("Accept", constant("*/*"))
            .setHeader("Authorization", constant("Basic " + edgeContributorAuthString))
            .to("{{edge.contributor.uri}}" + "/api/agreements" + "?bridgeEndpoint=true")
            .unmarshal().json(JsonLibrary.Jackson, Map.class)
            .bean(ExtractAgreementsProcessor.class)
            .marshal().json(JsonLibrary.Jackson, ArrayList.class)
            .setHeader("Access-Control-Allow-Origin", constant("*"))
            .setBody(body())
            .log("Response: ${body}");
        
        //predict the health state of userdata with machinelearning
        from("direct:predictHealthData").routeId("predictHealthData")
            .to("mongodb:myDb?database={{spring.data.mongodb.database}}&collection={{mongodb.user.data.collection}}&operation=findOneByQuery")
            .process(exchange -> {
                String id = exchange.getIn().getBody(Map.class).get("_id").toString();
                exchange.setProperty("id", id);
            })
            .setHeader(Exchange.HTTP_METHOD, constant("POST"))
            .setHeader(Exchange.CONTENT_TYPE, constant("application/json"))
            .marshal().json(JsonLibrary.Jackson, Map.class)
            .to("{{machinelearning.uri}}" + "/predict/")
            .process(exchange -> {
                ObjectId id = new ObjectId(exchange.getProperty("id", String.class));
                Document data = exchange.getIn().getBody(Document.class);
                data.replace("_id", id);
                exchange.getIn().setBody(data);
            })
            .to("mongodb:myDb?database={{spring.data.mongodb.database}}&collection={{mongodb.user.data.collection}}&operation=save")
            .log("Data successfully predicted ${date:now:dd-MM-yyyy HH:mm:ss}");
        
        //share the machinelearning hyperparameters with the edgenode Dataspace Connector
        from("timer://shareHyperparameters?period={{timer.period.hyperparameters}}").routeId("shareHyperparameters")
            .setHeader(Exchange.HTTP_METHOD, constant("GET"))
            .setHeader("Accept", constant("*/*"))
            .setHeader("Authorization", constant("Basic " + edgeContributorAuthString))
            .to("{{edge.contributor.uri}}" + "/api/offers")
            .choice()
                .when(simple("${body['_embedded']['resources'].size()} == 0"))
                    .to("direct:createResource")
                .otherwise()
                .setProperty("resourceHref", simple("${body['_embedded']['resources'][0]['_links']['self']['href']}"))
                    .process(exchange -> {
                        String href = exchange.getProperty("resourceHref", String.class);
                        String id = href.substring(href.lastIndexOf('/') + 1);
                        exchange.setProperty("resourceID", "offers/"+id);
                    })
                    .to("direct:getResourceArtifactID")
            .end()
            .to("direct:getHyperparameter")
            .log("Offered Hyperparameter: ${body}")
            .setHeader(Exchange.HTTP_METHOD, constant("PUT"))
            .setHeader(Exchange.CONTENT_TYPE, constant("application/json"))
            .process(exchange -> {
                Map artifact = new LinkedHashMap();
                artifact.put("title", exchange.getContext().resolvePropertyPlaceholders("{{resource.artifact.title}}"));
                artifact.put("description", exchange.getContext().resolvePropertyPlaceholders("{{resource.artifact.description}}"));
                artifact.put("value", exchange.getProperty("hyperparameters",  String.class));
                artifact.put("automatedDownload", exchange.getContext().resolvePropertyPlaceholders("{{resource.artifact.automateddownload}}"));
                exchange.getIn().setBody(artifact);
            })
            .marshal().json(JsonLibrary.Jackson)
            .toD("{{edge.contributor.uri}}" + "/api/artifacts/" + "${exchangeProperty.artifactID}")
            .log("Hyperparameters successfully shared");
        
        //recive the machinelearning hyperparameters from the edge node an set them in machinelearning
        from("timer://updateHyperparameters?period={{timer.period.hyperparameters}}").routeId("updateHyperparameters")
            .setHeader(Exchange.HTTP_METHOD, constant("GET"))
            .setHeader("Accept", constant("*/*"))
            .setHeader("Authorization", constant("Basic " + edgeContributorAuthString))
            .to("{{edge.contributor.uri}}" + "/api/requests")
            .choice()
                .when(simple("${body['_embedded']['resources'].size()} == 0"))
                    .to("direct:requestResource")
                .otherwise()
                    .setProperty("resourceHref", simple("${body['_embedded']['resources'][0]['_links']['self']['href']}"))
                    .process(exchange -> {
                        String href = exchange.getProperty("resourceHref", String.class);
                        String id = href.substring(href.lastIndexOf('/') + 1);
                        exchange.setProperty("resourceID", "requests/"+id);
                    })
                    .to("direct:getResourceArtifactID")
            .end()
            .toD("{{edge.contributor.uri}}" + "/api/artifacts/" +  "${exchangeProperty.artifactID}" + "/data/**")
            .log("Requested Hyperparameter: ${body}")
            .setHeader(Exchange.HTTP_METHOD, constant("POST"))
            .to("{{machinelearning.uri}}" + "/set_hyperparameters/")
            .log("Hyperparameters successfully update");;

        //get the machinelearning hyperparameters
        from("direct:getHyperparameter").routeId("getHyperparameters")
            .setHeader(Exchange.HTTP_METHOD, constant("GET"))
            .to("{{machinelearning.uri}}" + "/get_hyperparameters/")
            .convertBodyTo(Map.class)
            .marshal().json(JsonLibrary.Jackson)
            .setProperty("hyperparameters", simple("${body}"));
        
        //get the ArtifactID of an specific resource
        from("direct:getResourceArtifactID").routeId("getResourceArtifactID")
            .toD("{{edge.contributor.uri}}" + "/api/" + "${exchangeProperty.resourceID}" + "/representations")
            .setProperty("representationHref", simple("${body['_embedded']['representations'][0]['_links']['self']['href']}"))
            .process(exchange -> {
                String href = exchange.getProperty("representationHref", String.class);
                String id = href.substring(href.lastIndexOf('/') + 1);
                exchange.setProperty("representationID", id);
            })
            .toD("{{edge.contributor.uri}}" + "/api/representations/" + "${exchangeProperty.representationID}" + "/artifacts")
            .setProperty("artifactHref", simple("${body['_embedded']['artifacts'][0]['_links']['self']['href']}"))
            .process(exchange -> {
                String href = exchange.getProperty("artifactHref", String.class);
                String id = href.substring(href.lastIndexOf('/') + 1);
                exchange.setProperty("artifactID", id);
            });
        
        //create an resource offer to training coordinator
        from("direct:createResource").routeId("createResource")
            .log("create new resource offer")
            .setHeader(Exchange.HTTP_METHOD, constant("POST"))
            .setHeader("Accept", constant("*/*"))
            .setHeader(Exchange.CONTENT_TYPE, constant("application/json"))
            .setHeader("Authorization", constant("Basic " + edgeContributorAuthString))
            //create offer
            .process(exchange -> {
                Map offer = new LinkedHashMap();
                offer.put("title", exchange.getContext().resolvePropertyPlaceholders("{{resource.offer.title}}"));
                offer.put("description", exchange.getContext().resolvePropertyPlaceholders("{{resource.offer.description}}"));
                offer.put("keywords", exchange.getContext().resolvePropertyPlaceholders("{{resource.offer.keywords}}").split(","));
                offer.put("paymentModality", exchange.getContext().resolvePropertyPlaceholders("{{resource.offer.payment}}"));
                offer.put("publisher", exchange.getContext().resolvePropertyPlaceholders("{{resource.offer.publisher}}"));
                offer.put("language", exchange.getContext().resolvePropertyPlaceholders("{{resource.offer.language}}"));
                offer.put("license", exchange.getContext().resolvePropertyPlaceholders("{{resource.offer.license}}"));
                offer.put("sovereign", exchange.getContext().resolvePropertyPlaceholders("{{resource.offer.sovereign}}"));
                offer.put("endpointDocumentation", exchange.getContext().resolvePropertyPlaceholders("{{resource.offer.endpointdoc}}"));
                offer.put("key", "value");
                exchange.getIn().setBody(offer);
            })
            .marshal().json(JsonLibrary.Jackson)
            .to("{{edge.contributor.uri}}" + "/api/offers")
            .process(exchange -> {
                String location = exchange.getIn().getHeader("Location", String.class);
                String id = location.substring(location.lastIndexOf('/') + 1);
                exchange.setProperty("offerID", id);
            })
            .log("OfferID: ${exchangeProperty.offerID}")
            //create catalog
            .process(exchange -> {
                Map catalog = new LinkedHashMap();
                catalog.put("title", exchange.getContext().resolvePropertyPlaceholders("{{resource.catalog.title}}"));
                catalog.put("description", exchange.getContext().resolvePropertyPlaceholders("{{resource.catalog.description}}"));
                exchange.getIn().setBody(catalog);
            })
            .marshal().json(JsonLibrary.Jackson)
            .to("{{edge.contributor.uri}}" + "/api/catalogs")
            .process(exchange -> {
                String location = exchange.getIn().getHeader("Location", String.class);
                String id = location.substring(location.lastIndexOf('/') + 1);
                exchange.setProperty("catalogID", id);
            })
            .log("CatalogID: ${exchangeProperty.catalogID}")
            //bind offer with catalog
            .process(exchange -> {
                List<String> bind = new ArrayList<>();
                String offerString = exchange.getContext().resolvePropertyPlaceholders("{{edge.contributor.uri}}") + "/api/offer/" +  exchange.getProperty("offerID",  String.class);
                bind.add(offerString);
                exchange.getIn().setBody(bind);
            })
            .marshal().json(JsonLibrary.Jackson)
            .toD("{{edge.contributor.uri}}" + "/api/catalogs/" +  "${exchangeProperty.catalogID}" +"/offers")
            //create representation
            .process(exchange -> {
                Map representation = new LinkedHashMap();
                representation.put("title", exchange.getContext().resolvePropertyPlaceholders("{{resource.representation.title}}"));
                representation.put("description", exchange.getContext().resolvePropertyPlaceholders("{{resource.representation.description}}"));
                representation.put("mediaType", exchange.getContext().resolvePropertyPlaceholders("{{resource.representation.media}}"));
                representation.put("language", exchange.getContext().resolvePropertyPlaceholders("{{resource.representation.language}}"));
                representation.put("standard", "");
                exchange.getIn().setBody(representation);
            })
            .marshal().json(JsonLibrary.Jackson)
            .to("{{edge.contributor.uri}}" + "/api/representations")
            .process(exchange -> {
                String location = exchange.getIn().getHeader("Location", String.class);
                String id = location.substring(location.lastIndexOf('/') + 1);
                exchange.setProperty("representationID", id);
            })
            .log("RepresentationID: ${exchangeProperty.representationID}")
            .to("direct:getHyperparameter")
            //create artifact
            .process(exchange -> {
                Map artifact = new LinkedHashMap();
                artifact.put("title", exchange.getContext().resolvePropertyPlaceholders("{{resource.artifact.title}}"));
                artifact.put("description", exchange.getContext().resolvePropertyPlaceholders("{{resource.artifact.description}}"));
                artifact.put("value", exchange.getProperty("hyperparameters",  String.class));
                artifact.put("automatedDownload", exchange.getContext().resolvePropertyPlaceholders("{{resource.artifact.automateddownload}}"));
                exchange.getIn().setBody(artifact);
            })
            .marshal().json(JsonLibrary.Jackson)
            .setHeader(Exchange.HTTP_METHOD, constant("POST"))
            .to("{{edge.contributor.uri}}" + "/api/artifacts")
            .process(exchange -> {
                String location = exchange.getIn().getHeader("Location", String.class);
                String id = location.substring(location.lastIndexOf('/') + 1);
                exchange.setProperty("artifactID", id);
            })
            .log("ArtifactID: ${exchangeProperty.artifactID}")
            //bind represtentation with artifact
            .process(exchange -> {
                List<String> bind = new ArrayList<>();
                String offerString = exchange.getContext().resolvePropertyPlaceholders("{{edge.contributor.uri}}") + "/api/artifacts/" +  exchange.getProperty("artifactID",  String.class);
                bind.add(offerString);
                exchange.getIn().setBody(bind);
            })
            .marshal().json(JsonLibrary.Jackson)
            .toD("{{edge.contributor.uri}}" + "/api/representations/" +  "${exchangeProperty.representationID}" +"/artifacts")
            //bind offer with catalog
            .process(exchange -> {
                List<String> bind = new ArrayList<>();
                String offerString = exchange.getContext().resolvePropertyPlaceholders("{{edge.contributor.uri}}") + "/api/offer/" +  exchange.getProperty("offerID",  String.class);
                bind.add(offerString);
                exchange.getIn().setBody(bind);
            })
            .marshal().json(JsonLibrary.Jackson)
            .toD("{{edge.contributor.uri}}" + "/api/representations/" +  "${exchangeProperty.representationID}" +"/offers")
            //create contract
            .setProperty("contractStart", simple("${date:now:yyyy-MM-dd'T'HH:mm:ss.SSS'Z'}"))
            .setProperty("contractEnd", simple("${date:now+365d:yyyy-MM-dd'T'HH:mm:ss.SSS'Z'}"))
            .process(exchange -> {
                Map contract = new LinkedHashMap();
                contract.put("title", exchange.getContext().resolvePropertyPlaceholders("{{resource.contract.title}}"));
                contract.put("description", exchange.getContext().resolvePropertyPlaceholders("{{resource.contract.description}}"));
                contract.put("start", exchange.getProperty("contractStart",  String.class));
                contract.put("end", exchange.getProperty("contractEnd",  String.class));
                exchange.getIn().setBody(contract);
            })
            .marshal().json(JsonLibrary.Jackson)
            .to("{{edge.contributor.uri}}" + "/api/contracts")
            .process(exchange -> {
                String location = exchange.getIn().getHeader("Location", String.class);
                String id = location.substring(location.lastIndexOf('/') + 1);
                exchange.setProperty("contractID", id);
            })
            .log("ContractID: ${exchangeProperty.contractID}")
            //create rule
            .process(exchange -> {
                Map rule = new LinkedHashMap();
                rule.put("title", exchange.getContext().resolvePropertyPlaceholders("{{resource.rule.title}}"));
                rule.put("description", exchange.getContext().resolvePropertyPlaceholders("{{resource.rule.description}}"));
                rule.put("type", exchange.getContext().resolvePropertyPlaceholders("{{resource.rule.type}}"));
                exchange.getIn().setBody(rule);
            })
            .marshal().json(JsonLibrary.Jackson)
            .to("{{edge.contributor.uri}}" + "/api/examples/policy")
            .convertBodyTo(String.class)
            .marshal().json(JsonLibrary.Jackson)
            .setBody(simple("{\"value\": ${body}}"))
            .to("{{edge.contributor.uri}}" + "/api/rules")
            .process(exchange -> {
                String location = exchange.getIn().getHeader("Location", String.class);
                String id = location.substring(location.lastIndexOf('/') + 1);
                exchange.setProperty("ruleID", id);
            })
            .log("RuleID: ${exchangeProperty.ruleID}")
            //bind contract with rule
            .process(exchange -> {
                List<String> bind = new ArrayList<>();
                String offerString = exchange.getContext().resolvePropertyPlaceholders("{{edge.contributor.uri}}") + "/api/rules/" +  exchange.getProperty("ruleID",  String.class);
                bind.add(offerString);
                exchange.getIn().setBody(bind);
            })
            .marshal().json(JsonLibrary.Jackson)
            .toD("{{edge.contributor.uri}}" + "/api/contracts/" +  "${exchangeProperty.contractID}" +"/rules")
            //bind contract with offer
            .process(exchange -> {
                List<String> bind = new ArrayList<>();
                String offerString = exchange.getContext().resolvePropertyPlaceholders("{{edge.contributor.uri}}") + "/api/offers/" +  exchange.getProperty("offerID",  String.class);
                bind.add(offerString);
                exchange.getIn().setBody(bind);
            })
            .marshal().json(JsonLibrary.Jackson)
            .toD("{{edge.contributor.uri}}" + "/api/contracts/" +  "${exchangeProperty.contractID}" +"/offers")
            .log("new resource offer successfully created")
            .stop();
        
        //request an resource offer from training coordinator
        from("direct:requestResource").routeId("requestResource")
            .log("create new resource request")
            .setHeader(Exchange.HTTP_METHOD, constant("POST"))
            .setHeader("Accept", constant("*/*"))
            .setHeader("Authorization", constant("Basic " + edgeContributorAuthString))
            .setHeader(Exchange.HTTP_QUERY, simple("recipient="+ "{{training.coordinator.uri}}" + "/api/ids/data"))
            //get catalog ID
            .to("{{edge.contributor.uri}}" + "/api/ids/description")
            .choice()
                .when(simple("${body['ids:resourceCatalog']} == null"))
                    .log("No offer to request on")
                    .stop()
                .otherwise()
                    .setProperty("catalogId", simple("${body['ids:resourceCatalog'][0]['@id']}"))
            .end()
            //get recourceID and artifactID
            .setHeader(Exchange.HTTP_QUERY, simple("${headers.CamelHttpQuery}"+"&elementId="+ "${exchangeProperty.catalogId}"))
            .to("{{edge.contributor.uri}}" + "/api/ids/description")
            .setProperty("resourceId", simple("${body['ids:offeredResource'][0]['@id']}"))
            .setProperty("artifactId", simple("${body['ids:offeredResource'][0]['ids:representation'][0]['ids:instance'][0]['@id']}"))
            //negotiate contract
            .process(exchange -> {
                Map rule = new LinkedHashMap();
                rule.put("title", exchange.getContext().resolvePropertyPlaceholders("{{resource.rule.title}}"));
                rule.put("description", exchange.getContext().resolvePropertyPlaceholders("{{resource.rule.description}}"));
                rule.put("type", exchange.getContext().resolvePropertyPlaceholders("{{resource.rule.type}}"));
                exchange.getIn().setBody(rule);
            })
            .marshal().json(JsonLibrary.Jackson)
            .to("{{edge.contributor.uri}}" + "/api/examples/policy")
            .process(exchange -> {
                Map<String, Object> data = exchange.getIn().getBody(Map.class);
                List<Map> negotiationBody = new ArrayList<>();
                String target = exchange.getProperty("artifactId",  String.class);
                data.put("ids:target", target);
                negotiationBody.add(data);
                exchange.getIn().setBody(negotiationBody);
            })
            .marshal().json(JsonLibrary.Jackson)
            .setHeader(Exchange.HTTP_QUERY, simple("${headers.CamelHttpQuery}"+"&resourceIds="+ "${exchangeProperty.resourceId}"+"&artifactIds="+ "${exchangeProperty.artifactId}" + "&download=true"))
            .to("{{edge.contributor.uri}}" + "/api/ids/contract")
            .stop();
        
        //get health data in a spefic time interval from mongoDB
        from("jetty:http://0.0.0.0:8030/healthData").routeId("getHealthData")
            .choice()
                .when(simple("${header.start_date} regex '^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}(\\.\\d{3})?$' && ${header.end_date} regex '^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}(\\.\\d{3})?$'"))
                    .setHeader(MongoDbConstants.CRITERIA, simple("{eventTimestamp:{$gte:${header.start_date}, $lte:${header.end_date}}}"))
                .otherwise()
                    .setHeader(MongoDbConstants.CRITERIA, simple("{eventTimestamp:{$gte:'${header.start_date}T00:00:00.000Z', $lte:'${header.end_date}T23:59:59.999Z'}}"))
            .end()
            .setHeader(MongoDbConstants.SORT_BY, constant("{eventTimestamp: 1}"))
            .to("mongodb:myDb?database={{spring.data.mongodb.database}}&collection={{mongodb.user.data.collection}}&operation=findAll")
            .marshal().json(JsonLibrary.Jackson)
            .setBody(body())
            .setHeader("Access-Control-Allow-Origin", constant("*"));
        
        from("jetty:http://0.0.0.0:8030/triggerDataSynthesizer").routeId("triggerDataSynthesizer")
            .setHeader(Exchange.HTTP_METHOD, constant("POST"))
            .setHeader(Exchange.CONTENT_TYPE, constant("application/json"))
            .setBody(simple("{\"start_time\":\"${date:now-1d:dd/MM/yyyy}\", \"end_time\":\"${date:now:dd/MM/yyyy}\"}"))
            .to("{{datasynthesizer.uri}}" + "/synthesise_data_for_ui/" + "?bridgeEndpoint=true")
            .unmarshal().json(JsonLibrary.Jackson, Map.class)
            .to("mongodb:myDb?database={{spring.data.mongodb.database}}&collection={{mongodb.user.data.collection}}&operation=insert")
            .setHeader(Exchange.HTTP_RESPONSE_CODE, constant(200))
            .setBody(simple("{\"value\":\"Data Synthesizer triggerd\"}"))
            .setHeader("Access-Control-Allow-Origin", constant("*"));

        from("jetty:http://0.0.0.0:8030/getHyperparameters").routeId("displayHyperparameters")
            .setHeader(Exchange.HTTP_METHOD, constant("GET"))
            .to("{{machinelearning.uri}}" + "/get_hyperparameters/" + "?bridgeEndpoint=true")
            .setHeader("Access-Control-Allow-Origin", constant("*"));
        
        from("jetty:http://0.0.0.0:8030/startTraining").routeId("startTraining")
            .setHeader(Exchange.HTTP_METHOD, constant("GET"))
            .to("{{machinelearning.uri}}" + "/train/" + "?bridgeEndpoint=true")
            .setHeader("Access-Control-Allow-Origin", constant("*"));
            
    }
}

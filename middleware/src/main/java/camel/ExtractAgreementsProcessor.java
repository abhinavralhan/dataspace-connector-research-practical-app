package camel;

import org.apache.camel.Exchange;
import org.apache.camel.Processor;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import com.fasterxml.jackson.databind.ObjectMapper;

public class ExtractAgreementsProcessor implements Processor {

  public void process(Exchange exchange) throws Exception {
    Map data = exchange.getIn().getBody(Map.class);
    List<Map> agreements = (List<Map>) ((Map) data.get("_embedded")).get("agreements");
    List<Map> extractedAgreements = new ArrayList<>();
    for (Map agreement : agreements) {
        String value = (String) agreement.get("value");
        Map valueMap = new ObjectMapper().readValue(value, Map.class);
        Map extractedAgreement = new HashMap();
        extractedAgreement.put("contractCreationDate", agreement.get("creationDate"));
        extractedAgreement.put("agreementModificationDate", agreement.get("modificationDate"));
        extractedAgreement.put("agreementLink", ((Map) ((Map) agreement.get("_links")).get("self")).get("href"));
        extractedAgreement.put("consumer", ((Map) valueMap.get("ids:consumer")).get("@id"));
        extractedAgreement.put("provider", ((Map) valueMap.get("ids:provider")).get("@id"));
        extractedAgreement.put("contractStart", ((Map) valueMap.get("ids:contractStart")).get("@value"));
        extractedAgreement.put("contractEnd", ((Map) valueMap.get("ids:contractEnd")).get("@value"));
        extractedAgreement.put("permissionDescription", ((Map) ((List) ((Map) ((List) valueMap.get("ids:permission")).get(0)).get("ids:description")).get(0)).get("@value"));
        String artifactsLink = (String) extractedAgreement.get("agreementLink") + "/artifacts" + "?bridgeEndpoint=true";
        Map responseBody = exchange.getContext().createProducerTemplate().requestBodyAndHeaders(artifactsLink, null, exchange.getIn().getHeaders(),Map.class);
        List<Map> artifacts = (List<Map>) ((Map) responseBody.get("_embedded")).get("artifacts");
        Map firstArtifact = artifacts.get(0);
        extractedAgreement.put("artifactModificationDate", firstArtifact.get("modificationDate"));
        extractedAgreement.put("artifactTitle", firstArtifact.get("title"));
        extractedAgreement.put("artifactDescription", firstArtifact.get("description"));

        extractedAgreements.add(extractedAgreement);
    }
    exchange.getOut().setBody(extractedAgreements);
  }
}
FROM maven:3.8.7-eclipse-temurin-17 AS build 
RUN mkdir -p /app
WORKDIR /app
COPY src ./src  
COPY pom.xml . 
RUN mvn -f ./pom.xml -DskipTests clean package

FROM openjdk:17
RUN mkdir -p /app
WORKDIR /app
COPY --from=build app/target/middleware-1.0-SNAPSHOT.jar /app/middleware-1.0-SNAPSHOT.jar
EXPOSE 8030
CMD ["java", "-jar", "middleware-1.0-SNAPSHOT.jar"]
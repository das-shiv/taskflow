FROM maven:3.9-eclipse-temurin-21 AS build
WORKDIR /workspace
COPY pom.xml .
COPY src src
RUN mvn -B -DskipTests package

FROM eclipse-temurin:21-jre-alpine
RUN addgroup -S taskflow && adduser -S taskflow -G taskflow
WORKDIR /app
COPY --from=build /workspace/target/task-service-0.1.0.jar app.jar
USER taskflow
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "/app/app.jar"]


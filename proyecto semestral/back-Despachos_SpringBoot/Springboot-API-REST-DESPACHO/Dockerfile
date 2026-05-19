# Etapa 1: compilación del JAR
FROM maven:3.9-eclipse-temurin-17 AS builder
WORKDIR /build
COPY pom.xml .
COPY src ./src
RUN mvn -q clean package -DskipTests

# Etapa 2: imagen de ejecución
FROM eclipse-temurin:17-jre-alpine
RUN apk add --no-cache netcat-openbsd \
    && addgroup -g 1001 appgroup \
    && adduser -u 1001 -G appgroup -D appuser

WORKDIR /app
COPY --from=builder /build/target/*.jar app.jar
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh && chown -R appuser:appgroup /app

USER appuser
EXPOSE 8081
ENTRYPOINT ["/entrypoint.sh"]

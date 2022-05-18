package computerdatabase;

import static io.gatling.javaapi.core.CoreDsl.*;
import static io.gatling.javaapi.http.HttpDsl.*;

import io.gatling.javaapi.core.*;
import io.gatling.javaapi.http.*;
import java.time.Duration;


public class GatlingScenario extends Simulation {

  FeederBuilder<String> feeder = csv("users.csv");
  int concurrency = 10;
  int transactions_ps = 500;
  int time_limit = 60;


  HttpProtocolBuilder httpProtocol =
      http
          .baseUrl("http://localhost:8080")
          .acceptHeader("text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8")
          .doNotTrackHeader("1")
          .acceptLanguageHeader("en-US,en;q=0.5")
          .acceptEncodingHeader("gzip, deflate")
          .userAgentHeader(
              "Gatling/3.7.6");

  ScenarioBuilder scn =
      scenario("Basic Test")
          .feed(feeder)
          .exec(http("request_2").get("/add/#{userId}"))
          .exec(http("request_3").get("/has/#{userId}"))
          .exec(http("request_3").get("/remove/#{userId}"))
          //.exec(http("request_4").get("/status/"))
          ;

  {
    setUp(scn.injectOpen(atOnceUsers(concurrency),constantUsersPerSec(transactions_ps).during(time_limit)).protocols(httpProtocol));
  }
}

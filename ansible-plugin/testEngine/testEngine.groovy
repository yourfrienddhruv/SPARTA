@Grab('org.springframework.boot:spring-boot-starter-actuator:1.2.0.RELEASE')
@Grab('org.springframework.boot:spring-boot-starter-jdbc:1.2.0.RELEASE')
@Grab("org.codehaus.groovy:groovy-all:2.3.7")
@Grab("h2")

import org.springframework.web.bind.annotation.RequestMapping
import org.springframework.web.bind.annotation.RequestParam
import org.springframework.web.bind.annotation.ResponseBody
import org.springframework.web.bind.annotation.RestController

import javax.servlet.http.HttpServletResponse
import javax.management.remote.JMXConnectorFactory
import javax.management.remote.JMXConnectorFactory
import javax.management.remote.JMXServiceURL
import java.sql.*

@RestController
class ServiceController {

    @Autowired
    JdbcTemplate jdbcTemplate

    @RequestMapping("/checkJMX")
    String checkJmx(@RequestParam String address, @RequestParam String bean) {
        //String address = "localhost:9001"
        //String bean = "org.hornetq:module=JMS,type=Queue,name=\"MyQueue\""
        //?address={address}&bean={bean}&attribute={attribute}
        def serverUrl = "service:jmx:rmi:///jndi/rmi://" + address + "/jmxrmi"
        def server = JMXConnectorFactory.connect(new JMXServiceURL(serverUrl))
        //make sure to reconnect in case the jvm was restrated
        server.connect()
        GroovyMBean mbean = new GroovyMBean(server.MBeanServerConnection, bean)
        return "${mbean.ExpiryAddress},${mbean.MessageCount}"
        server.close()
    }


    @RequestMapping("/scneario1_validation_users")
    @ResponseBody
    String scneario1_validation_users(HttpServletResponse response) {
    		List rows = jdbcTemplate.queryForList("SELECT * FROM CSVREAD('scenario1_golddata.csv') where Name='Rasmeet'");
        for(r in rows){
    		  print r
          return "OK"
        }
        //failures
        response.setStatus(HttpServletResponse.SC_BAD_REQUEST);
    }


}

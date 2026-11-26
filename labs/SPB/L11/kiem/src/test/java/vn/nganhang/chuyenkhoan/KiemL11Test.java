package vn.nganhang.chuyenkhoan;

import static org.hamcrest.Matchers.containsString;
import static org.hamcrest.Matchers.not;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.content;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.header;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import org.junit.jupiter.api.Test;
import org.slf4j.MDC;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.micrometer.metrics.test.autoconfigure.AutoConfigureMetrics;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.webmvc.test.autoconfigure.AutoConfigureMockMvc;
import org.springframework.test.web.servlet.MockMvc;

@SpringBootTest
@AutoConfigureMockMvc
@AutoConfigureMetrics
class KiemL11Test {
    @Autowired MockMvc mvc;

    @Test
    void echoesCorrelationIdAndCleansMdc() throws Exception {
        mvc.perform(post("/api/v1/obs-transfers?amount=50000").header("X-Correlation-Id", "cid-9988"))
            .andExpect(status().isCreated())
            .andExpect(header().string("X-Correlation-Id", "cid-9988"))
            .andExpect(jsonPath("$.correlationId").value("cid-9988"));
        assertNull(MDC.get("correlationId"));
    }

    @Test
    void generatesCorrelationIdWhenMissing() throws Exception {
        mvc.perform(post("/api/v1/obs-transfers?amount=1000"))
            .andExpect(status().isCreated())
            .andExpect(header().exists("X-Correlation-Id"));
    }

    @Test
    void prometheusExposesBoundedTagWithoutHighCardinality() throws Exception {
        mvc.perform(post("/api/v1/obs-transfers?amount=2000")).andExpect(status().isCreated());
        mvc.perform(get("/actuator/prometheus"))
            .andExpect(status().isOk())
            .andExpect(content().string(containsString("bank_transfers_total{")))
            .andExpect(content().string(not(containsString("correlationId="))));
    }
}

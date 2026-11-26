package vn.nganhang.chuyenkhoan;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.webmvc.test.autoconfigure.AutoConfigureMockMvc;
import org.springframework.test.web.servlet.MockMvc;

@SpringBootTest
@AutoConfigureMockMvc
class KiemL00Test {
    @Autowired MockMvc mvc;

    @Test
    void healthEndpointReturnsUpAndBoot413() throws Exception {
        mvc.perform(get("/api/v1/health"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.status").value("UP"))
            .andExpect(jsonPath("$.service").value("chuyen-khoan"))
            .andExpect(jsonPath("$.boot").value("4.1.3"));
    }

    @Test
    void unknownPathReturns404() throws Exception {
        mvc.perform(get("/api/v1/unknown")).andExpect(status().isNotFound());
    }

    @Test
    void javaVersionIsAtLeast21() {
        org.junit.jupiter.api.Assertions.assertTrue(Runtime.version().feature() >= 21);
    }
}

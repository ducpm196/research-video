package vn.nganhang.chuyenkhoan;

import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.webmvc.test.autoconfigure.WebMvcTest;
import org.springframework.http.MediaType;
import org.springframework.test.context.bean.override.mockito.MockitoBean;
import org.springframework.test.web.servlet.MockMvc;

@WebMvcTest(UnitTransferController.class)
class KiemL09WebTest {
    @Autowired MockMvc mvc;
    @MockitoBean UnitTransferService service;

    @Test
    void webSliceReturns201FromMockService() throws Exception {
        when(service.execute("A", "B", 50_000L)).thenReturn("OK:A->B:50000");
        mvc.perform(post("/api/v1/unit-transfers")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"fromId\":\"A\",\"toId\":\"B\",\"amount\":50000}"))
            .andExpect(status().isCreated())
            .andExpect(jsonPath("$.receipt").value("OK:A->B:50000"));
    }

    @Test
    void invalidPayloadRejectedAtWebSlice() throws Exception {
        mvc.perform(post("/api/v1/unit-transfers")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"fromId\":\"\",\"toId\":\"B\",\"amount\":-5}"))
            .andExpect(status().isBadRequest());
    }
}

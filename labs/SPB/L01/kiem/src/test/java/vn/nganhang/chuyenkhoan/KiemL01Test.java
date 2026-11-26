package vn.nganhang.chuyenkhoan;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.content;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.webmvc.test.autoconfigure.AutoConfigureMockMvc;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

@SpringBootTest
@AutoConfigureMockMvc
class KiemL01Test {
    @Autowired MockMvc mvc;

    @Test
    void validTransferReturns201() throws Exception {
        mvc.perform(post("/api/v1/transfers")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"fromAccount\":\"TK01\",\"toAccount\":\"TK02\",\"amount\":250000}"))
            .andExpect(status().isCreated())
            .andExpect(jsonPath("$.status").value("ACCEPTED"))
            .andExpect(jsonPath("$.amount").value(250000));
    }

    @Test
    void zeroAmountReturnsRfc9457ProblemDetail() throws Exception {
        mvc.perform(post("/api/v1/transfers")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"fromAccount\":\"TK01\",\"toAccount\":\"TK02\",\"amount\":0}"))
            .andExpect(status().isBadRequest())
            .andExpect(content().contentTypeCompatibleWith(MediaType.APPLICATION_PROBLEM_JSON))
            .andExpect(jsonPath("$.status").value(400))
            .andExpect(jsonPath("$.errors").isArray());
    }

    @Test
    void negativeAmountReturns400() throws Exception {
        mvc.perform(post("/api/v1/transfers")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"fromAccount\":\"TK01\",\"toAccount\":\"TK02\",\"amount\":-10}"))
            .andExpect(status().isBadRequest())
            .andExpect(jsonPath("$.title").value("Validation Error"));
    }

    @Test
    void blankAccountReturns400() throws Exception {
        mvc.perform(post("/api/v1/transfers")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"fromAccount\":\"\",\"toAccount\":\"TK02\",\"amount\":50000}"))
            .andExpect(status().isBadRequest());
    }
}

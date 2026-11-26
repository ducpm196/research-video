package vn.nganhang.chuyenkhoan;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.time.Instant;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.webmvc.test.autoconfigure.AutoConfigureMockMvc;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

@SpringBootTest
@AutoConfigureMockMvc
class KiemL08Test {
    @Autowired MockMvc mvc;
    @Autowired JwtService jwt;

    @Test
    void missingOrTamperedJwtReturns401() throws Exception {
        mvc.perform(post("/api/v1/transfers").contentType(MediaType.APPLICATION_JSON)
                .content("{\"fromAccount\":\"TK-AN\",\"toAccount\":\"TK-BINH\",\"amount\":1000}"))
            .andExpect(status().isUnauthorized());

        String bad = jwt.sign("an", "TELLER", Instant.now().getEpochSecond() + 300) + "x";
        mvc.perform(post("/api/v1/transfers").header("Authorization", "Bearer " + bad)
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"fromAccount\":\"TK-AN\",\"toAccount\":\"TK-BINH\",\"amount\":1000}"))
            .andExpect(status().isUnauthorized());
    }

    @Test
    void expiredJwtReturns401() throws Exception {
        String expTok = jwt.sign("an", "TELLER", Instant.now().getEpochSecond() - 60);
        mvc.perform(post("/api/v1/transfers").header("Authorization", "Bearer " + expTok)
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"fromAccount\":\"TK-AN\",\"toAccount\":\"TK-BINH\",\"amount\":1000}"))
            .andExpect(status().isUnauthorized());
    }

    @Test
    void viewerRoleGets403() throws Exception {
        String tok = jwt.sign("an", "VIEWER", Instant.now().getEpochSecond() + 300);
        mvc.perform(post("/api/v1/transfers").header("Authorization", "Bearer " + tok)
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"fromAccount\":\"TK-AN\",\"toAccount\":\"TK-BINH\",\"amount\":1000}"))
            .andExpect(status().isForbidden());
    }

    @Test
    void tellerBolaBlockedAcrossOwnersAndAllowedOnOwnAccount() throws Exception {
        String tok = jwt.sign("an", "TELLER", Instant.now().getEpochSecond() + 300);
        mvc.perform(post("/api/v1/transfers").header("Authorization", "Bearer " + tok)
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"fromAccount\":\"TK-BINH\",\"toAccount\":\"TK-AN\",\"amount\":1000}"))
            .andExpect(status().isForbidden());

        mvc.perform(post("/api/v1/transfers").header("Authorization", "Bearer " + tok)
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"fromAccount\":\"TK-AN\",\"toAccount\":\"TK-BINH\",\"amount\":1000}"))
            .andExpect(status().isCreated())
            .andExpect(jsonPath("$.status").value("ACCEPTED"));
    }
}

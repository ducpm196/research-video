package vn.nganhang.chuyenkhoan;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
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
class KiemL07Test {
    @Autowired MockMvc mvc;

    @Test
    void openApiDocsContainsTransferPaths() throws Exception {
        mvc.perform(get("/v3/api-docs"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.openapi").value(org.hamcrest.Matchers.startsWith("3.")))
            .andExpect(jsonPath("$.paths['/api/v1/transfers'].get").exists())
            .andExpect(jsonPath("$.paths['/api/v2/transfers'].post").exists());
    }

    @Test
    void cursorPaginationStrictlySkipsCursorId() throws Exception {
        mvc.perform(get("/api/v1/transfers?cursor=5&limit=3"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.items.length()").value(3))
            .andExpect(jsonPath("$.items[0].id").value(6))
            .andExpect(jsonPath("$.items[2].id").value(8))
            .andExpect(jsonPath("$.nextCursor").value(8))
            .andExpect(jsonPath("$.hasMore").value(true));
    }

    @Test
    void v2AcceptsOmittedOptionalChannelForBackwardCompatibility() throws Exception {
        mvc.perform(post("/api/v2/transfers")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"fromAccount\":\"TK01\",\"toAccount\":\"TK02\",\"amount\":150000}"))
            .andExpect(status().isCreated())
            .andExpect(jsonPath("$.channel").value("MOBILE"));
    }
}

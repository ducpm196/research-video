package vn.nganhang.chuyenkhoan;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.nio.file.Files;
import java.nio.file.Path;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.webmvc.test.autoconfigure.AutoConfigureMockMvc;
import org.springframework.test.web.servlet.MockMvc;

@SpringBootTest
@AutoConfigureMockMvc
class KiemL12Test {
    @Autowired MockMvc mvc;

    @Test
    void multiStageDockerfileUsesJreNonRootAndMaxRamPct() throws Exception {
        String df = Files.readString(Path.of("Dockerfile"));
        long fromCount = df.lines().filter(l -> l.trim().startsWith("FROM ")).count();
        assertTrue(fromCount >= 2, "Phai dung Dockerfile nhieu tang >= 2 FROM");
        assertTrue(df.contains("eclipse-temurin:21-jre"), "Tang chay phai dung JRE");
        assertTrue(df.contains("USER "), "Phai chay bang user khong phai root");
        assertTrue(df.contains("-XX:MaxRAMPercentage=75"), "Phai dat MaxRAMPercentage=75");
    }

    @Test
    void ciWorkflowRunsMavenVerify() throws Exception {
        String ci = Files.readString(Path.of(".github/workflows/ci.yml"));
        assertTrue(ci.contains("./mvnw -B verify"));
        assertTrue(ci.contains("21"));
    }

    @Test
    void runtimeEndpointWorks() throws Exception {
        assertEquals(384L, RuntimeProfileController.maxHeapMiB(512, 75.0));
        mvc.perform(get("/api/v1/runtime"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.maxHeapMiB512_75pct").value(384));
    }
}

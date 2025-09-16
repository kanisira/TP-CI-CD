package com.example.demo.user;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

import java.util.List;

import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@WebMvcTest(UserController.class)
class UserControllerTest {

    @Autowired
    private MockMvc mvc;

    @MockBean
    private UserRepository repo;

    @Test
    void listUsers_returnsOkAndJsonArray() throws Exception {
        User u = new User();
        u.setName("Alice");
        u.setEmail("alice@example.com");
        when(repo.findAll()).thenReturn(List.of(u));

        mvc.perform(get("/api/users"))
                .andExpect(status().isOk())
                .andExpect(content().contentTypeCompatibleWith(MediaType.APPLICATION_JSON))
                .andExpect(jsonPath("$[0].name").value("Alice"));
    }

    @Test
    void createUser_returns201() throws Exception {
        User u = new User();
        u.setName("Bob");
        u.setEmail("bob@example.com");
        when(repo.save(org.mockito.ArgumentMatchers.any(User.class))).thenReturn(u);

        mvc.perform(post("/api/users")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"name\":\"Bob\",\"email\":\"bob@example.com\"}"))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.name").value("Bob"));
    }
}

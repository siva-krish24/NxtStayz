//
// Source code recreated from a .class file by IntelliJ IDEA
// (powered by FernFlower decompiler)
//

package com.example.nxtstayz;

import com.example.nxtstayz.model.Hotel;
import com.example.nxtstayz.model.Room;
import com.example.nxtstayz.repository.HotelJpaRepository;
import com.example.nxtstayz.repository.RoomJpaRepository;
import java.util.HashMap;
import org.hamcrest.Matchers;
import org.junit.Assert;
import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.MethodOrderer;
import org.junit.jupiter.api.Order;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.TestInstance;
import org.junit.jupiter.api.TestMethodOrder;
import org.junit.jupiter.api.TestInstance.Lifecycle;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.jdbc.AutoConfigureTestDatabase;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.test.context.jdbc.Sql;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.request.MockHttpServletRequestBuilder;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;
import org.springframework.test.web.servlet.result.MockMvcResultMatchers;

@SpringBootTest
@AutoConfigureMockMvc
@AutoConfigureTestDatabase
@TestInstance(Lifecycle.PER_CLASS)
@TestMethodOrder(MethodOrderer.OrderAnnotation.class)
@Sql(
    scripts = {"/schema.sql", "/data.sql"}
)
public class NxtStayzControllerTests {
    @Autowired
    private MockMvc mockMvc;
    @Autowired
    private RoomJpaRepository roomJpaRepository;
    @Autowired
    private HotelJpaRepository hotelJpaRepository;
    @Autowired
    private JdbcTemplate jdbcTemplate;
    private HashMap<Integer, Object[]> hotelsHashMap = new HashMap();
    private HashMap<Integer, Object[]> roomsHashMap;

    public NxtStayzControllerTests() {
        this.hotelsHashMap.put(1, new Object[]{"The Plaza Hotel", "New York", 4});
        this.hotelsHashMap.put(2, new Object[]{"The Beverly Hills Hotel", "Los Angeles", 5});
        this.hotelsHashMap.put(3, new Object[]{"The Langham", "Chicago", 3});
        this.hotelsHashMap.put(4, new Object[]{"Fontain Miami Beach", "Miami", 4});
        this.hotelsHashMap.put(5, new Object[]{"Fontainebleau Miami Beach", "Miami", 5});
        this.roomsHashMap = new HashMap();
        this.roomsHashMap.put(1, new Object[]{"A-101", "Deluxe Room", 375.0, 1});
        this.roomsHashMap.put(2, new Object[]{"A-205", "Suite", 950.0, 1});
        this.roomsHashMap.put(3, new Object[]{"B-106", "Penthouse Suite", 2500.0, 1});
        this.roomsHashMap.put(4, new Object[]{"C-401", "Superior Guest Room", 465.0, 2});
        this.roomsHashMap.put(5, new Object[]{"D-202", "Bungalow", 1250.0, 2});
        this.roomsHashMap.put(6, new Object[]{"A-107", "Penthouse Suite", 3300.0, 2});
        this.roomsHashMap.put(7, new Object[]{"A-301", "Grand Room", 410.0, 3});
        this.roomsHashMap.put(8, new Object[]{"C-313", "Executive Suite", 700.0, 3});
        this.roomsHashMap.put(9, new Object[]{"D-404", "Premier Suite", 880.0, 3});
        this.roomsHashMap.put(10, new Object[]{"D-201", "Ocean Room", 300.0, 2});
        this.roomsHashMap.put(11, new Object[]{"D-401", "Oceanfront Room", 350.0, 4});
    }

    @Test
    @Order(1)
    public void testGetHotels() throws Exception {
        this.mockMvc.perform(MockMvcRequestBuilders.get("/hotels", new Object[0])).andExpect(MockMvcResultMatchers.status().isOk()).andExpect(MockMvcResultMatchers.jsonPath("$", Matchers.hasSize(3))).andExpect(MockMvcResultMatchers.jsonPath("$[0].hotelId", Matchers.equalTo(1))).andExpect(MockMvcResultMatchers.jsonPath("$[0].hotelName", Matchers.equalTo(((Object[])this.hotelsHashMap.get(1))[0]))).andExpect(MockMvcResultMatchers.jsonPath("$[0].location", Matchers.equalTo(((Object[])this.hotelsHashMap.get(1))[1]))).andExpect(MockMvcResultMatchers.jsonPath("$[0].rating", Matchers.equalTo(((Object[])this.hotelsHashMap.get(1))[2]))).andExpect(MockMvcResultMatchers.jsonPath("$[1].hotelId", Matchers.equalTo(2))).andExpect(MockMvcResultMatchers.jsonPath("$[1].hotelName", Matchers.equalTo(((Object[])this.hotelsHashMap.get(2))[0]))).andExpect(MockMvcResultMatchers.jsonPath("$[1].location", Matchers.equalTo(((Object[])this.hotelsHashMap.get(2))[1]))).andExpect(MockMvcResultMatchers.jsonPath("$[1].rating", Matchers.equalTo(((Object[])this.hotelsHashMap.get(2))[2]))).andExpect(MockMvcResultMatchers.jsonPath("$[2].hotelId", Matchers.equalTo(3))).andExpect(MockMvcResultMatchers.jsonPath("$[2].hotelName", Matchers.equalTo(((Object[])this.hotelsHashMap.get(3))[0]))).andExpect(MockMvcResultMatchers.jsonPath("$[2].location", Matchers.equalTo(((Object[])this.hotelsHashMap.get(3))[1]))).andExpect(MockMvcResultMatchers.jsonPath("$[2].rating", Matchers.equalTo(((Object[])this.hotelsHashMap.get(3))[2])));
    }

    @Test
    @Order(2)
    public void testGetHotelNotFound() throws Exception {
        this.mockMvc.perform(MockMvcRequestBuilders.get("/hotels/48", new Object[0])).andExpect(MockMvcResultMatchers.status().isNotFound());
    }

    @Test
    @Order(3)
    public void testGetHotelById() throws Exception {
        this.mockMvc.perform(MockMvcRequestBuilders.get("/hotels/1", new Object[0])).andExpect(MockMvcResultMatchers.status().isOk()).andExpect(MockMvcResultMatchers.jsonPath("$", Matchers.notNullValue())).andExpect(MockMvcResultMatchers.jsonPath("$.hotelId", Matchers.equalTo(1))).andExpect(MockMvcResultMatchers.jsonPath("$.hotelName", Matchers.equalTo(((Object[])this.hotelsHashMap.get(1))[0]))).andExpect(MockMvcResultMatchers.jsonPath("$.location", Matchers.equalTo(((Object[])this.hotelsHashMap.get(1))[1]))).andExpect(MockMvcResultMatchers.jsonPath("$.rating", Matchers.equalTo(((Object[])this.hotelsHashMap.get(1))[2])));
        this.mockMvc.perform(MockMvcRequestBuilders.get("/hotels/2", new Object[0])).andExpect(MockMvcResultMatchers.status().isOk()).andExpect(MockMvcResultMatchers.jsonPath("$", Matchers.notNullValue())).andExpect(MockMvcResultMatchers.jsonPath("$.hotelId", Matchers.equalTo(2))).andExpect(MockMvcResultMatchers.jsonPath("$.hotelName", Matchers.equalTo(((Object[])this.hotelsHashMap.get(2))[0]))).andExpect(MockMvcResultMatchers.jsonPath("$.location", Matchers.equalTo(((Object[])this.hotelsHashMap.get(2))[1]))).andExpect(MockMvcResultMatchers.jsonPath("$.rating", Matchers.equalTo(((Object[])this.hotelsHashMap.get(2))[2])));
        this.mockMvc.perform(MockMvcRequestBuilders.get("/hotels/3", new Object[0])).andExpect(MockMvcResultMatchers.status().isOk()).andExpect(MockMvcResultMatchers.jsonPath("$", Matchers.notNullValue())).andExpect(MockMvcResultMatchers.jsonPath("$.hotelId", Matchers.equalTo(3))).andExpect(MockMvcResultMatchers.jsonPath("$.hotelName", Matchers.equalTo(((Object[])this.hotelsHashMap.get(3))[0]))).andExpect(MockMvcResultMatchers.jsonPath("$.location", Matchers.equalTo(((Object[])this.hotelsHashMap.get(3))[1]))).andExpect(MockMvcResultMatchers.jsonPath("$.rating", Matchers.equalTo(((Object[])this.hotelsHashMap.get(3))[2])));
    }

    @Test
    @Order(4)
    public void testPostHotel() throws Exception {
        String content = "{\n    \"hotelName\": \"" + ((Object[])this.hotelsHashMap.get(4))[0] + "\",\n    \"location\": \"" + ((Object[])this.hotelsHashMap.get(4))[1] + "\",\n    \"rating\": " + ((Object[])this.hotelsHashMap.get(4))[2] + "\n}";
        MockHttpServletRequestBuilder mockRequest = MockMvcRequestBuilders.post("/hotels", new Object[0]).contentType(MediaType.APPLICATION_JSON).accept(new MediaType[]{MediaType.APPLICATION_JSON}).content(content);
        this.mockMvc.perform(mockRequest).andExpect(MockMvcResultMatchers.status().isOk()).andExpect(MockMvcResultMatchers.jsonPath("$", Matchers.notNullValue())).andExpect(MockMvcResultMatchers.jsonPath("$.hotelId", Matchers.equalTo(4))).andExpect(MockMvcResultMatchers.jsonPath("$.hotelName", Matchers.equalTo(((Object[])this.hotelsHashMap.get(4))[0]))).andExpect(MockMvcResultMatchers.jsonPath("$.location", Matchers.equalTo(((Object[])this.hotelsHashMap.get(4))[1]))).andExpect(MockMvcResultMatchers.jsonPath("$.rating", Matchers.equalTo(((Object[])this.hotelsHashMap.get(4))[2])));
    }

    @Test
    @Order(5)
    public void testAfterPostHotel() throws Exception {
        this.mockMvc.perform(MockMvcRequestBuilders.get("/hotels/4", new Object[0])).andExpect(MockMvcResultMatchers.status().isOk()).andExpect(MockMvcResultMatchers.jsonPath("$", Matchers.notNullValue())).andExpect(MockMvcResultMatchers.jsonPath("$.hotelId", Matchers.equalTo(4))).andExpect(MockMvcResultMatchers.jsonPath("$.hotelName", Matchers.equalTo(((Object[])this.hotelsHashMap.get(4))[0]))).andExpect(MockMvcResultMatchers.jsonPath("$.location", Matchers.equalTo(((Object[])this.hotelsHashMap.get(4))[1]))).andExpect(MockMvcResultMatchers.jsonPath("$.rating", Matchers.equalTo(((Object[])this.hotelsHashMap.get(4))[2])));
    }

    @Test
    @Order(6)
    public void testDbAfterPostHotel() throws Exception {
        Hotel hotel = (Hotel)this.hotelJpaRepository.findById(4).get();
        Assert.assertEquals((long)hotel.getHotelId(), 4L);
        Assert.assertEquals(hotel.getHotelName(), ((Object[])this.hotelsHashMap.get(4))[0]);
        Assert.assertEquals(hotel.getLocation(), ((Object[])this.hotelsHashMap.get(4))[1]);
        Assert.assertEquals(hotel.getRating(), ((Object[])this.hotelsHashMap.get(4))[2]);
    }

    @Test
    @Order(7)
    public void testPutHotelNotFound() throws Exception {
        String content = "{\n    \"hotelName\": \"" + ((Object[])this.hotelsHashMap.get(5))[0] + "\",\n    \"location\": \"" + ((Object[])this.hotelsHashMap.get(5))[1] + "\",\n    \"rating\": " + ((Object[])this.hotelsHashMap.get(5))[2] + "\n}";
        MockHttpServletRequestBuilder mockRequest = MockMvcRequestBuilders.put("/hotels/48", new Object[0]).contentType(MediaType.APPLICATION_JSON).accept(new MediaType[]{MediaType.APPLICATION_JSON}).content(content);
        this.mockMvc.perform(mockRequest).andExpect(MockMvcResultMatchers.status().isNotFound());
    }

    @Test
    @Order(8)
    public void testPutHotel() throws Exception {
        String content = "{\n    \"hotelName\": \"" + ((Object[])this.hotelsHashMap.get(5))[0] + "\",\n    \"location\": \"" + ((Object[])this.hotelsHashMap.get(5))[1] + "\",\n    \"rating\": " + ((Object[])this.hotelsHashMap.get(5))[2] + "\n}";
        MockHttpServletRequestBuilder mockRequest = MockMvcRequestBuilders.put("/hotels/4", new Object[0]).contentType(MediaType.APPLICATION_JSON).accept(new MediaType[]{MediaType.APPLICATION_JSON}).content(content);
        this.mockMvc.perform(mockRequest).andExpect(MockMvcResultMatchers.status().isOk()).andExpect(MockMvcResultMatchers.jsonPath("$", Matchers.notNullValue())).andExpect(MockMvcResultMatchers.jsonPath("$.hotelId", Matchers.equalTo(4))).andExpect(MockMvcResultMatchers.jsonPath("$.hotelName", Matchers.equalTo(((Object[])this.hotelsHashMap.get(5))[0]))).andExpect(MockMvcResultMatchers.jsonPath("$.location", Matchers.equalTo(((Object[])this.hotelsHashMap.get(5))[1]))).andExpect(MockMvcResultMatchers.jsonPath("$.rating", Matchers.equalTo(((Object[])this.hotelsHashMap.get(5))[2])));
    }

    @Test
    @Order(9)
    public void testAfterPutHotel() throws Exception {
        this.mockMvc.perform(MockMvcRequestBuilders.get("/hotels/4", new Object[0])).andExpect(MockMvcResultMatchers.status().isOk()).andExpect(MockMvcResultMatchers.jsonPath("$", Matchers.notNullValue())).andExpect(MockMvcResultMatchers.jsonPath("$.hotelId", Matchers.equalTo(4))).andExpect(MockMvcResultMatchers.jsonPath("$.hotelName", Matchers.equalTo(((Object[])this.hotelsHashMap.get(5))[0]))).andExpect(MockMvcResultMatchers.jsonPath("$.location", Matchers.equalTo(((Object[])this.hotelsHashMap.get(5))[1]))).andExpect(MockMvcResultMatchers.jsonPath("$.rating", Matchers.equalTo(((Object[])this.hotelsHashMap.get(5))[2])));
    }

    @Test
    @Order(10)
    public void testDbAfterPutHotel() throws Exception {
        Hotel hotel = (Hotel)this.hotelJpaRepository.findById(4).get();
        Assert.assertEquals((long)hotel.getHotelId(), 4L);
        Assert.assertEquals(hotel.getHotelName(), ((Object[])this.hotelsHashMap.get(5))[0]);
        Assert.assertEquals(hotel.getLocation(), ((Object[])this.hotelsHashMap.get(5))[1]);
        Assert.assertEquals(hotel.getRating(), ((Object[])this.hotelsHashMap.get(5))[2]);
    }

    @Test
    @Order(11)
    public void testGetRooms() throws Exception {
        this.mockMvc.perform(MockMvcRequestBuilders.get("/hotels/rooms", new Object[0])).andExpect(MockMvcResultMatchers.status().isOk()).andExpect(MockMvcResultMatchers.jsonPath("$", Matchers.hasSize(9))).andExpect(MockMvcResultMatchers.jsonPath("$[0].roomId", Matchers.equalTo(1))).andExpect(MockMvcResultMatchers.jsonPath("$[0].roomNumber", Matchers.equalTo(((Object[])this.roomsHashMap.get(1))[0]))).andExpect(MockMvcResultMatchers.jsonPath("$[0].roomType", Matchers.equalTo(((Object[])this.roomsHashMap.get(1))[1]))).andExpect(MockMvcResultMatchers.jsonPath("$[0].price", Matchers.equalTo(((Object[])this.roomsHashMap.get(1))[2]))).andExpect(MockMvcResultMatchers.jsonPath("$[0].hotel.hotelId", Matchers.equalTo(((Object[])this.roomsHashMap.get(1))[3]))).andExpect(MockMvcResultMatchers.jsonPath("$[1].roomId", Matchers.equalTo(2))).andExpect(MockMvcResultMatchers.jsonPath("$[1].roomNumber", Matchers.equalTo(((Object[])this.roomsHashMap.get(2))[0]))).andExpect(MockMvcResultMatchers.jsonPath("$[1].roomType", Matchers.equalTo(((Object[])this.roomsHashMap.get(2))[1]))).andExpect(MockMvcResultMatchers.jsonPath("$[1].price", Matchers.equalTo(((Object[])this.roomsHashMap.get(2))[2]))).andExpect(MockMvcResultMatchers.jsonPath("$[1].hotel.hotelId", Matchers.equalTo(((Object[])this.roomsHashMap.get(2))[3]))).andExpect(MockMvcResultMatchers.jsonPath("$[2].roomId", Matchers.equalTo(3))).andExpect(MockMvcResultMatchers.jsonPath("$[2].roomNumber", Matchers.equalTo(((Object[])this.roomsHashMap.get(3))[0]))).andExpect(MockMvcResultMatchers.jsonPath("$[2].roomType", Matchers.equalTo(((Object[])this.roomsHashMap.get(3))[1]))).andExpect(MockMvcResultMatchers.jsonPath("$[2].price", Matchers.equalTo(((Object[])this.roomsHashMap.get(3))[2]))).andExpect(MockMvcResultMatchers.jsonPath("$[2].hotel.hotelId", Matchers.equalTo(((Object[])this.roomsHashMap.get(3))[3]))).andExpect(MockMvcResultMatchers.jsonPath("$[3].roomId", Matchers.equalTo(4))).andExpect(MockMvcResultMatchers.jsonPath("$[3].roomNumber", Matchers.equalTo(((Object[])this.roomsHashMap.get(4))[0]))).andExpect(MockMvcResultMatchers.jsonPath("$[3].roomType", Matchers.equalTo(((Object[])this.roomsHashMap.get(4))[1]))).andExpect(MockMvcResultMatchers.jsonPath("$[3].price", Matchers.equalTo(((Object[])this.roomsHashMap.get(4))[2]))).andExpect(MockMvcResultMatchers.jsonPath("$[3].hotel.hotelId", Matchers.equalTo(((Object[])this.roomsHashMap.get(4))[3]))).andExpect(MockMvcResultMatchers.jsonPath("$[4].roomId", Matchers.equalTo(5))).andExpect(MockMvcResultMatchers.jsonPath("$[4].roomNumber", Matchers.equalTo(((Object[])this.roomsHashMap.get(5))[0]))).andExpect(MockMvcResultMatchers.jsonPath("$[4].roomType", Matchers.equalTo(((Object[])this.roomsHashMap.get(5))[1]))).andExpect(MockMvcResultMatchers.jsonPath("$[4].price", Matchers.equalTo(((Object[])this.roomsHashMap.get(5))[2]))).andExpect(MockMvcResultMatchers.jsonPath("$[4].hotel.hotelId", Matchers.equalTo(((Object[])this.roomsHashMap.get(5))[3]))).andExpect(MockMvcResultMatchers.jsonPath("$[5].roomId", Matchers.equalTo(6))).andExpect(MockMvcResultMatchers.jsonPath("$[5].roomNumber", Matchers.equalTo(((Object[])this.roomsHashMap.get(6))[0]))).andExpect(MockMvcResultMatchers.jsonPath("$[5].roomType", Matchers.equalTo(((Object[])this.roomsHashMap.get(6))[1]))).andExpect(MockMvcResultMatchers.jsonPath("$[5].price", Matchers.equalTo(((Object[])this.roomsHashMap.get(6))[2]))).andExpect(MockMvcResultMatchers.jsonPath("$[5].hotel.hotelId", Matchers.equalTo(((Object[])this.roomsHashMap.get(6))[3]))).andExpect(MockMvcResultMatchers.jsonPath("$[6].roomId", Matchers.equalTo(7))).andExpect(MockMvcResultMatchers.jsonPath("$[6].roomNumber", Matchers.equalTo(((Object[])this.roomsHashMap.get(7))[0]))).andExpect(MockMvcResultMatchers.jsonPath("$[6].roomType", Matchers.equalTo(((Object[])this.roomsHashMap.get(7))[1]))).andExpect(MockMvcResultMatchers.jsonPath("$[6].price", Matchers.equalTo(((Object[])this.roomsHashMap.get(7))[2]))).andExpect(MockMvcResultMatchers.jsonPath("$[6].hotel.hotelId", Matchers.equalTo(((Object[])this.roomsHashMap.get(7))[3]))).andExpect(MockMvcResultMatchers.jsonPath("$[7].roomId", Matchers.equalTo(8))).andExpect(MockMvcResultMatchers.jsonPath("$[7].roomNumber", Matchers.equalTo(((Object[])this.roomsHashMap.get(8))[0]))).andExpect(MockMvcResultMatchers.jsonPath("$[7].roomType", Matchers.equalTo(((Object[])this.roomsHashMap.get(8))[1]))).andExpect(MockMvcResultMatchers.jsonPath("$[7].price", Matchers.equalTo(((Object[])this.roomsHashMap.get(8))[2]))).andExpect(MockMvcResultMatchers.jsonPath("$[7].hotel.hotelId", Matchers.equalTo(((Object[])this.roomsHashMap.get(8))[3]))).andExpect(MockMvcResultMatchers.jsonPath("$[8].roomId", Matchers.equalTo(9))).andExpect(MockMvcResultMatchers.jsonPath("$[8].roomNumber", Matchers.equalTo(((Object[])this.roomsHashMap.get(9))[0]))).andExpect(MockMvcResultMatchers.jsonPath("$[8].roomType", Matchers.equalTo(((Object[])this.roomsHashMap.get(9))[1]))).andExpect(MockMvcResultMatchers.jsonPath("$[8].price", Matchers.equalTo(((Object[])this.roomsHashMap.get(9))[2]))).andExpect(MockMvcResultMatchers.jsonPath("$[8].hotel.hotelId", Matchers.equalTo(((Object[])this.roomsHashMap.get(9))[3])));
    }

    @Test
    @Order(12)
    public void testGetRoomNotFound() throws Exception {
        this.mockMvc.perform(MockMvcRequestBuilders.get("/hotels/rooms/48", new Object[0])).andExpect(MockMvcResultMatchers.status().isNotFound());
    }

    @Test
    @Order(13)
    public void testGetRoomById() throws Exception {
        this.mockMvc.perform(MockMvcRequestBuilders.get("/hotels/rooms/1", new Object[0])).andExpect(MockMvcResultMatchers.status().isOk()).andExpect(MockMvcResultMatchers.jsonPath("$.roomId", Matchers.equalTo(1))).andExpect(MockMvcResultMatchers.jsonPath("$.roomNumber", Matchers.equalTo(((Object[])this.roomsHashMap.get(1))[0]))).andExpect(MockMvcResultMatchers.jsonPath("$.roomType", Matchers.equalTo(((Object[])this.roomsHashMap.get(1))[1]))).andExpect(MockMvcResultMatchers.jsonPath("$.price", Matchers.equalTo(((Object[])this.roomsHashMap.get(1))[2]))).andExpect(MockMvcResultMatchers.jsonPath("$.hotel.hotelId", Matchers.equalTo(((Object[])this.roomsHashMap.get(1))[3])));
        this.mockMvc.perform(MockMvcRequestBuilders.get("/hotels/rooms/2", new Object[0])).andExpect(MockMvcResultMatchers.status().isOk()).andExpect(MockMvcResultMatchers.jsonPath("$.roomId", Matchers.equalTo(2))).andExpect(MockMvcResultMatchers.jsonPath("$.roomNumber", Matchers.equalTo(((Object[])this.roomsHashMap.get(2))[0]))).andExpect(MockMvcResultMatchers.jsonPath("$.roomType", Matchers.equalTo(((Object[])this.roomsHashMap.get(2))[1]))).andExpect(MockMvcResultMatchers.jsonPath("$.price", Matchers.equalTo(((Object[])this.roomsHashMap.get(2))[2]))).andExpect(MockMvcResultMatchers.jsonPath("$.hotel.hotelId", Matchers.equalTo(((Object[])this.roomsHashMap.get(2))[3])));
        this.mockMvc.perform(MockMvcRequestBuilders.get("/hotels/rooms/3", new Object[0])).andExpect(MockMvcResultMatchers.status().isOk()).andExpect(MockMvcResultMatchers.jsonPath("$.roomId", Matchers.equalTo(3))).andExpect(MockMvcResultMatchers.jsonPath("$.roomNumber", Matchers.equalTo(((Object[])this.roomsHashMap.get(3))[0]))).andExpect(MockMvcResultMatchers.jsonPath("$.roomType", Matchers.equalTo(((Object[])this.roomsHashMap.get(3))[1]))).andExpect(MockMvcResultMatchers.jsonPath("$.price", Matchers.equalTo(((Object[])this.roomsHashMap.get(3))[2]))).andExpect(MockMvcResultMatchers.jsonPath("$.hotel.hotelId", Matchers.equalTo(((Object[])this.roomsHashMap.get(3))[3])));
        this.mockMvc.perform(MockMvcRequestBuilders.get("/hotels/rooms/4", new Object[0])).andExpect(MockMvcResultMatchers.status().isOk()).andExpect(MockMvcResultMatchers.jsonPath("$.roomId", Matchers.equalTo(4))).andExpect(MockMvcResultMatchers.jsonPath("$.roomNumber", Matchers.equalTo(((Object[])this.roomsHashMap.get(4))[0]))).andExpect(MockMvcResultMatchers.jsonPath("$.roomType", Matchers.equalTo(((Object[])this.roomsHashMap.get(4))[1]))).andExpect(MockMvcResultMatchers.jsonPath("$.price", Matchers.equalTo(((Object[])this.roomsHashMap.get(4))[2]))).andExpect(MockMvcResultMatchers.jsonPath("$.hotel.hotelId", Matchers.equalTo(((Object[])this.roomsHashMap.get(4))[3])));
        this.mockMvc.perform(MockMvcRequestBuilders.get("/hotels/rooms/5", new Object[0])).andExpect(MockMvcResultMatchers.status().isOk()).andExpect(MockMvcResultMatchers.jsonPath("$.roomId", Matchers.equalTo(5))).andExpect(MockMvcResultMatchers.jsonPath("$.roomNumber", Matchers.equalTo(((Object[])this.roomsHashMap.get(5))[0]))).andExpect(MockMvcResultMatchers.jsonPath("$.roomType", Matchers.equalTo(((Object[])this.roomsHashMap.get(5))[1]))).andExpect(MockMvcResultMatchers.jsonPath("$.price", Matchers.equalTo(((Object[])this.roomsHashMap.get(5))[2]))).andExpect(MockMvcResultMatchers.jsonPath("$.hotel.hotelId", Matchers.equalTo(((Object[])this.roomsHashMap.get(5))[3])));
        this.mockMvc.perform(MockMvcRequestBuilders.get("/hotels/rooms/6", new Object[0])).andExpect(MockMvcResultMatchers.status().isOk()).andExpect(MockMvcResultMatchers.jsonPath("$.roomId", Matchers.equalTo(6))).andExpect(MockMvcResultMatchers.jsonPath("$.roomNumber", Matchers.equalTo(((Object[])this.roomsHashMap.get(6))[0]))).andExpect(MockMvcResultMatchers.jsonPath("$.roomType", Matchers.equalTo(((Object[])this.roomsHashMap.get(6))[1]))).andExpect(MockMvcResultMatchers.jsonPath("$.price", Matchers.equalTo(((Object[])this.roomsHashMap.get(6))[2]))).andExpect(MockMvcResultMatchers.jsonPath("$.hotel.hotelId", Matchers.equalTo(((Object[])this.roomsHashMap.get(6))[3])));
        this.mockMvc.perform(MockMvcRequestBuilders.get("/hotels/rooms/7", new Object[0])).andExpect(MockMvcResultMatchers.status().isOk()).andExpect(MockMvcResultMatchers.jsonPath("$.roomId", Matchers.equalTo(7))).andExpect(MockMvcResultMatchers.jsonPath("$.roomNumber", Matchers.equalTo(((Object[])this.roomsHashMap.get(7))[0]))).andExpect(MockMvcResultMatchers.jsonPath("$.roomType", Matchers.equalTo(((Object[])this.roomsHashMap.get(7))[1]))).andExpect(MockMvcResultMatchers.jsonPath("$.price", Matchers.equalTo(((Object[])this.roomsHashMap.get(7))[2]))).andExpect(MockMvcResultMatchers.jsonPath("$.hotel.hotelId", Matchers.equalTo(((Object[])this.roomsHashMap.get(7))[3])));
        this.mockMvc.perform(MockMvcRequestBuilders.get("/hotels/rooms/8", new Object[0])).andExpect(MockMvcResultMatchers.status().isOk()).andExpect(MockMvcResultMatchers.jsonPath("$.roomId", Matchers.equalTo(8))).andExpect(MockMvcResultMatchers.jsonPath("$.roomNumber", Matchers.equalTo(((Object[])this.roomsHashMap.get(8))[0]))).andExpect(MockMvcResultMatchers.jsonPath("$.roomType", Matchers.equalTo(((Object[])this.roomsHashMap.get(8))[1]))).andExpect(MockMvcResultMatchers.jsonPath("$.price", Matchers.equalTo(((Object[])this.roomsHashMap.get(8))[2]))).andExpect(MockMvcResultMatchers.jsonPath("$.hotel.hotelId", Matchers.equalTo(((Object[])this.roomsHashMap.get(8))[3])));
        this.mockMvc.perform(MockMvcRequestBuilders.get("/hotels/rooms/9", new Object[0])).andExpect(MockMvcResultMatchers.status().isOk()).andExpect(MockMvcResultMatchers.jsonPath("$.roomId", Matchers.equalTo(9))).andExpect(MockMvcResultMatchers.jsonPath("$.roomNumber", Matchers.equalTo(((Object[])this.roomsHashMap.get(9))[0]))).andExpect(MockMvcResultMatchers.jsonPath("$.roomType", Matchers.equalTo(((Object[])this.roomsHashMap.get(9))[1]))).andExpect(MockMvcResultMatchers.jsonPath("$.price", Matchers.equalTo(((Object[])this.roomsHashMap.get(9))[2]))).andExpect(MockMvcResultMatchers.jsonPath("$.hotel.hotelId", Matchers.equalTo(((Object[])this.roomsHashMap.get(9))[3])));
    }

    @Test
    @Order(14)
    public void testPostRoom() throws Exception {
        String content = "{\n    \"roomNumber\": \"" + ((Object[])this.roomsHashMap.get(10))[0] + "\",\n    \"roomType\": \"" + ((Object[])this.roomsHashMap.get(10))[1] + "\",\n    \"price\": " + ((Object[])this.roomsHashMap.get(10))[2] + ",\n    \"hotel\": {\n        \"hotelId\": " + ((Object[])this.roomsHashMap.get(10))[3] + "\n    }\n}";
        MockHttpServletRequestBuilder mockRequest = MockMvcRequestBuilders.post("/hotels/rooms", new Object[0]).contentType(MediaType.APPLICATION_JSON).accept(new MediaType[]{MediaType.APPLICATION_JSON}).content(content);
        this.mockMvc.perform(mockRequest).andExpect(MockMvcResultMatchers.status().isOk()).andExpect(MockMvcResultMatchers.jsonPath("$", Matchers.notNullValue())).andExpect(MockMvcResultMatchers.jsonPath("$.roomId", Matchers.equalTo(10))).andExpect(MockMvcResultMatchers.jsonPath("$.roomNumber", Matchers.equalTo(((Object[])this.roomsHashMap.get(10))[0]))).andExpect(MockMvcResultMatchers.jsonPath("$.roomType", Matchers.equalTo(((Object[])this.roomsHashMap.get(10))[1]))).andExpect(MockMvcResultMatchers.jsonPath("$.price", Matchers.equalTo(((Object[])this.roomsHashMap.get(10))[2]))).andExpect(MockMvcResultMatchers.jsonPath("$.hotel.hotelId", Matchers.equalTo(((Object[])this.roomsHashMap.get(10))[3])));
    }

    @Test
    @Order(15)
    public void testAfterPostRoom() throws Exception {
        this.mockMvc.perform(MockMvcRequestBuilders.get("/hotels/rooms/10", new Object[0])).andExpect(MockMvcResultMatchers.status().isOk()).andExpect(MockMvcResultMatchers.jsonPath("$", Matchers.notNullValue())).andExpect(MockMvcResultMatchers.jsonPath("$.roomId", Matchers.equalTo(10))).andExpect(MockMvcResultMatchers.jsonPath("$.roomNumber", Matchers.equalTo(((Object[])this.roomsHashMap.get(10))[0]))).andExpect(MockMvcResultMatchers.jsonPath("$.roomType", Matchers.equalTo(((Object[])this.roomsHashMap.get(10))[1]))).andExpect(MockMvcResultMatchers.jsonPath("$.price", Matchers.equalTo(((Object[])this.roomsHashMap.get(10))[2]))).andExpect(MockMvcResultMatchers.jsonPath("$.hotel.hotelId", Matchers.equalTo(((Object[])this.roomsHashMap.get(10))[3])));
    }

    @Test
    @Order(16)
    public void testDbAfterPostRoom() throws Exception {
        Room room = (Room)this.roomJpaRepository.findById(10).get();
        Assert.assertEquals((long)room.getRoomId(), 10L);
        Assert.assertEquals(room.getRoomNumber(), ((Object[])this.roomsHashMap.get(10))[0]);
        Assert.assertEquals(room.getRoomType(), ((Object[])this.roomsHashMap.get(10))[1]);
        Assert.assertEquals(room.getPrice(), ((Object[])this.roomsHashMap.get(10))[2]);
        Assert.assertEquals(room.getHotel().getHotelId(), ((Object[])this.roomsHashMap.get(10))[3]);
    }

    @Test
    @Order(17)
    public void testPutRoomNotFound() throws Exception {
        String content = "{\n    \"roomNumber\": \"" + ((Object[])this.roomsHashMap.get(11))[0] + "\",\n    \"roomType\": \"" + ((Object[])this.roomsHashMap.get(11))[1] + "\",\n    \"price\": " + ((Object[])this.roomsHashMap.get(11))[2] + ",\n    \"hotel\": {\n        \"hotelId\": " + ((Object[])this.roomsHashMap.get(11))[3] + "\n    }\n}";
        MockHttpServletRequestBuilder mockRequest = MockMvcRequestBuilders.put("/hotels/rooms/48", new Object[0]).contentType(MediaType.APPLICATION_JSON).accept(new MediaType[]{MediaType.APPLICATION_JSON}).content(content);
        this.mockMvc.perform(mockRequest).andExpect(MockMvcResultMatchers.status().isNotFound());
    }

    @Test
    @Order(18)
    public void testPutRoom() throws Exception {
        String content = "{\n    \"roomNumber\": \"" + ((Object[])this.roomsHashMap.get(11))[0] + "\",\n    \"roomType\": \"" + ((Object[])this.roomsHashMap.get(11))[1] + "\",\n    \"price\": " + ((Object[])this.roomsHashMap.get(11))[2] + ",\n    \"hotel\": {\n        \"hotelId\": " + ((Object[])this.roomsHashMap.get(11))[3] + "\n    }\n}";
        MockHttpServletRequestBuilder mockRequest = MockMvcRequestBuilders.put("/hotels/rooms/10", new Object[0]).contentType(MediaType.APPLICATION_JSON).accept(new MediaType[]{MediaType.APPLICATION_JSON}).content(content);
        this.mockMvc.perform(mockRequest).andExpect(MockMvcResultMatchers.status().isOk()).andExpect(MockMvcResultMatchers.jsonPath("$", Matchers.notNullValue())).andExpect(MockMvcResultMatchers.jsonPath("$.roomId", Matchers.equalTo(10))).andExpect(MockMvcResultMatchers.jsonPath("$.roomNumber", Matchers.equalTo(((Object[])this.roomsHashMap.get(11))[0]))).andExpect(MockMvcResultMatchers.jsonPath("$.roomType", Matchers.equalTo(((Object[])this.roomsHashMap.get(11))[1]))).andExpect(MockMvcResultMatchers.jsonPath("$.price", Matchers.equalTo(((Object[])this.roomsHashMap.get(11))[2]))).andExpect(MockMvcResultMatchers.jsonPath("$.hotel.hotelId", Matchers.equalTo(((Object[])this.roomsHashMap.get(11))[3])));
    }

    @Test
    @Order(19)
    public void testAfterPutRoom() throws Exception {
        this.mockMvc.perform(MockMvcRequestBuilders.get("/hotels/rooms/10", new Object[0])).andExpect(MockMvcResultMatchers.status().isOk()).andExpect(MockMvcResultMatchers.jsonPath("$", Matchers.notNullValue())).andExpect(MockMvcResultMatchers.jsonPath("$.roomId", Matchers.equalTo(10))).andExpect(MockMvcResultMatchers.jsonPath("$.roomNumber", Matchers.equalTo(((Object[])this.roomsHashMap.get(11))[0]))).andExpect(MockMvcResultMatchers.jsonPath("$.roomType", Matchers.equalTo(((Object[])this.roomsHashMap.get(11))[1]))).andExpect(MockMvcResultMatchers.jsonPath("$.price", Matchers.equalTo(((Object[])this.roomsHashMap.get(11))[2]))).andExpect(MockMvcResultMatchers.jsonPath("$.hotel.hotelId", Matchers.equalTo(((Object[])this.roomsHashMap.get(11))[3])));
    }

    @Test
    @Order(20)
    public void testDbAfterPutRoom() throws Exception {
        Room room = (Room)this.roomJpaRepository.findById(10).get();
        Assert.assertEquals((long)room.getRoomId(), 10L);
        Assert.assertEquals(room.getRoomNumber(), ((Object[])this.roomsHashMap.get(11))[0]);
        Assert.assertEquals(room.getRoomType(), ((Object[])this.roomsHashMap.get(11))[1]);
        Assert.assertEquals(room.getPrice(), ((Object[])this.roomsHashMap.get(11))[2]);
        Assert.assertEquals(room.getHotel().getHotelId(), ((Object[])this.roomsHashMap.get(11))[3]);
    }

    @Test
    @Order(21)
    public void testDeleteHotelNotFound() throws Exception {
        MockHttpServletRequestBuilder mockRequest = MockMvcRequestBuilders.delete("/hotels/148", new Object[0]).contentType(MediaType.APPLICATION_JSON);
        this.mockMvc.perform(mockRequest).andExpect(MockMvcResultMatchers.status().isNotFound());
    }

    @Test
    @Order(22)
    public void testDeleteHotel() throws Exception {
        MockHttpServletRequestBuilder mockRequest = MockMvcRequestBuilders.delete("/hotels/4", new Object[0]).contentType(MediaType.APPLICATION_JSON);
        this.mockMvc.perform(mockRequest).andExpect(MockMvcResultMatchers.status().isNoContent());
    }

    @Test
    @Order(23)
    public void testAfterDeleteHotel() throws Exception {
        this.mockMvc.perform(MockMvcRequestBuilders.get("/hotels", new Object[0])).andExpect(MockMvcResultMatchers.status().isOk()).andExpect(MockMvcResultMatchers.jsonPath("$", Matchers.hasSize(3))).andExpect(MockMvcResultMatchers.jsonPath("$[0].hotelId", Matchers.equalTo(1))).andExpect(MockMvcResultMatchers.jsonPath("$[0].hotelName", Matchers.equalTo(((Object[])this.hotelsHashMap.get(1))[0]))).andExpect(MockMvcResultMatchers.jsonPath("$[0].location", Matchers.equalTo(((Object[])this.hotelsHashMap.get(1))[1]))).andExpect(MockMvcResultMatchers.jsonPath("$[0].rating", Matchers.equalTo(((Object[])this.hotelsHashMap.get(1))[2]))).andExpect(MockMvcResultMatchers.jsonPath("$[1].hotelId", Matchers.equalTo(2))).andExpect(MockMvcResultMatchers.jsonPath("$[1].hotelName", Matchers.equalTo(((Object[])this.hotelsHashMap.get(2))[0]))).andExpect(MockMvcResultMatchers.jsonPath("$[1].location", Matchers.equalTo(((Object[])this.hotelsHashMap.get(2))[1]))).andExpect(MockMvcResultMatchers.jsonPath("$[1].rating", Matchers.equalTo(((Object[])this.hotelsHashMap.get(2))[2]))).andExpect(MockMvcResultMatchers.jsonPath("$[2].hotelId", Matchers.equalTo(3))).andExpect(MockMvcResultMatchers.jsonPath("$[2].hotelName", Matchers.equalTo(((Object[])this.hotelsHashMap.get(3))[0]))).andExpect(MockMvcResultMatchers.jsonPath("$[2].location", Matchers.equalTo(((Object[])this.hotelsHashMap.get(3))[1]))).andExpect(MockMvcResultMatchers.jsonPath("$[2].rating", Matchers.equalTo(((Object[])this.hotelsHashMap.get(3))[2])));
        this.mockMvc.perform(MockMvcRequestBuilders.get("/hotels/rooms/10", new Object[0])).andExpect(MockMvcResultMatchers.status().isOk()).andExpect(MockMvcResultMatchers.jsonPath("$.roomId", Matchers.equalTo(10))).andExpect(MockMvcResultMatchers.jsonPath("$.roomNumber", Matchers.equalTo(((Object[])this.roomsHashMap.get(11))[0]))).andExpect(MockMvcResultMatchers.jsonPath("$.roomType", Matchers.equalTo(((Object[])this.roomsHashMap.get(11))[1]))).andExpect(MockMvcResultMatchers.jsonPath("$.price", Matchers.equalTo(((Object[])this.roomsHashMap.get(11))[2]))).andExpect(MockMvcResultMatchers.jsonPath("$.hotel.hotelId", new Object[0]).doesNotExist());
    }

    @Test
    @Order(24)
    public void testDeleteRoomNotFound() throws Exception {
        MockHttpServletRequestBuilder mockRequest = MockMvcRequestBuilders.delete("/hotels/rooms/148", new Object[0]).contentType(MediaType.APPLICATION_JSON);
        this.mockMvc.perform(mockRequest).andExpect(MockMvcResultMatchers.status().isNotFound());
    }

    @Test
    @Order(25)
    public void testDeleteRoom() throws Exception {
        MockHttpServletRequestBuilder mockRequest = MockMvcRequestBuilders.delete("/hotels/rooms/10", new Object[0]).contentType(MediaType.APPLICATION_JSON);
        this.mockMvc.perform(mockRequest).andExpect(MockMvcResultMatchers.status().isNoContent());
    }

    @Test
    @Order(26)
    public void testAfterDeleteRoom() throws Exception {
        this.mockMvc.perform(MockMvcRequestBuilders.get("/hotels/rooms", new Object[0])).andExpect(MockMvcResultMatchers.status().isOk()).andExpect(MockMvcResultMatchers.jsonPath("$", Matchers.hasSize(9))).andExpect(MockMvcResultMatchers.jsonPath("$[0].roomId", Matchers.equalTo(1))).andExpect(MockMvcResultMatchers.jsonPath("$[0].roomNumber", Matchers.equalTo(((Object[])this.roomsHashMap.get(1))[0]))).andExpect(MockMvcResultMatchers.jsonPath("$[0].roomType", Matchers.equalTo(((Object[])this.roomsHashMap.get(1))[1]))).andExpect(MockMvcResultMatchers.jsonPath("$[0].price", Matchers.equalTo(((Object[])this.roomsHashMap.get(1))[2]))).andExpect(MockMvcResultMatchers.jsonPath("$[0].hotel.hotelId", Matchers.equalTo(((Object[])this.roomsHashMap.get(1))[3]))).andExpect(MockMvcResultMatchers.jsonPath("$[1].roomId", Matchers.equalTo(2))).andExpect(MockMvcResultMatchers.jsonPath("$[1].roomNumber", Matchers.equalTo(((Object[])this.roomsHashMap.get(2))[0]))).andExpect(MockMvcResultMatchers.jsonPath("$[1].roomType", Matchers.equalTo(((Object[])this.roomsHashMap.get(2))[1]))).andExpect(MockMvcResultMatchers.jsonPath("$[1].price", Matchers.equalTo(((Object[])this.roomsHashMap.get(2))[2]))).andExpect(MockMvcResultMatchers.jsonPath("$[1].hotel.hotelId", Matchers.equalTo(((Object[])this.roomsHashMap.get(2))[3]))).andExpect(MockMvcResultMatchers.jsonPath("$[2].roomId", Matchers.equalTo(3))).andExpect(MockMvcResultMatchers.jsonPath("$[2].roomNumber", Matchers.equalTo(((Object[])this.roomsHashMap.get(3))[0]))).andExpect(MockMvcResultMatchers.jsonPath("$[2].roomType", Matchers.equalTo(((Object[])this.roomsHashMap.get(3))[1]))).andExpect(MockMvcResultMatchers.jsonPath("$[2].price", Matchers.equalTo(((Object[])this.roomsHashMap.get(3))[2]))).andExpect(MockMvcResultMatchers.jsonPath("$[2].hotel.hotelId", Matchers.equalTo(((Object[])this.roomsHashMap.get(3))[3]))).andExpect(MockMvcResultMatchers.jsonPath("$[3].roomId", Matchers.equalTo(4))).andExpect(MockMvcResultMatchers.jsonPath("$[3].roomNumber", Matchers.equalTo(((Object[])this.roomsHashMap.get(4))[0]))).andExpect(MockMvcResultMatchers.jsonPath("$[3].roomType", Matchers.equalTo(((Object[])this.roomsHashMap.get(4))[1]))).andExpect(MockMvcResultMatchers.jsonPath("$[3].price", Matchers.equalTo(((Object[])this.roomsHashMap.get(4))[2]))).andExpect(MockMvcResultMatchers.jsonPath("$[3].hotel.hotelId", Matchers.equalTo(((Object[])this.roomsHashMap.get(4))[3]))).andExpect(MockMvcResultMatchers.jsonPath("$[4].roomId", Matchers.equalTo(5))).andExpect(MockMvcResultMatchers.jsonPath("$[4].roomNumber", Matchers.equalTo(((Object[])this.roomsHashMap.get(5))[0]))).andExpect(MockMvcResultMatchers.jsonPath("$[4].roomType", Matchers.equalTo(((Object[])this.roomsHashMap.get(5))[1]))).andExpect(MockMvcResultMatchers.jsonPath("$[4].price", Matchers.equalTo(((Object[])this.roomsHashMap.get(5))[2]))).andExpect(MockMvcResultMatchers.jsonPath("$[4].hotel.hotelId", Matchers.equalTo(((Object[])this.roomsHashMap.get(5))[3]))).andExpect(MockMvcResultMatchers.jsonPath("$[5].roomId", Matchers.equalTo(6))).andExpect(MockMvcResultMatchers.jsonPath("$[5].roomNumber", Matchers.equalTo(((Object[])this.roomsHashMap.get(6))[0]))).andExpect(MockMvcResultMatchers.jsonPath("$[5].roomType", Matchers.equalTo(((Object[])this.roomsHashMap.get(6))[1]))).andExpect(MockMvcResultMatchers.jsonPath("$[5].price", Matchers.equalTo(((Object[])this.roomsHashMap.get(6))[2]))).andExpect(MockMvcResultMatchers.jsonPath("$[5].hotel.hotelId", Matchers.equalTo(((Object[])this.roomsHashMap.get(6))[3]))).andExpect(MockMvcResultMatchers.jsonPath("$[6].roomId", Matchers.equalTo(7))).andExpect(MockMvcResultMatchers.jsonPath("$[6].roomNumber", Matchers.equalTo(((Object[])this.roomsHashMap.get(7))[0]))).andExpect(MockMvcResultMatchers.jsonPath("$[6].roomType", Matchers.equalTo(((Object[])this.roomsHashMap.get(7))[1]))).andExpect(MockMvcResultMatchers.jsonPath("$[6].price", Matchers.equalTo(((Object[])this.roomsHashMap.get(7))[2]))).andExpect(MockMvcResultMatchers.jsonPath("$[6].hotel.hotelId", Matchers.equalTo(((Object[])this.roomsHashMap.get(7))[3]))).andExpect(MockMvcResultMatchers.jsonPath("$[7].roomId", Matchers.equalTo(8))).andExpect(MockMvcResultMatchers.jsonPath("$[7].roomNumber", Matchers.equalTo(((Object[])this.roomsHashMap.get(8))[0]))).andExpect(MockMvcResultMatchers.jsonPath("$[7].roomType", Matchers.equalTo(((Object[])this.roomsHashMap.get(8))[1]))).andExpect(MockMvcResultMatchers.jsonPath("$[7].price", Matchers.equalTo(((Object[])this.roomsHashMap.get(8))[2]))).andExpect(MockMvcResultMatchers.jsonPath("$[7].hotel.hotelId", Matchers.equalTo(((Object[])this.roomsHashMap.get(8))[3]))).andExpect(MockMvcResultMatchers.jsonPath("$[8].roomId", Matchers.equalTo(9))).andExpect(MockMvcResultMatchers.jsonPath("$[8].roomNumber", Matchers.equalTo(((Object[])this.roomsHashMap.get(9))[0]))).andExpect(MockMvcResultMatchers.jsonPath("$[8].roomType", Matchers.equalTo(((Object[])this.roomsHashMap.get(9))[1]))).andExpect(MockMvcResultMatchers.jsonPath("$[8].price", Matchers.equalTo(((Object[])this.roomsHashMap.get(9))[2]))).andExpect(MockMvcResultMatchers.jsonPath("$[8].hotel.hotelId", Matchers.equalTo(((Object[])this.roomsHashMap.get(9))[3])));
    }

    @Test
    @Order(27)
    public void testGetHotelByRoomId() throws Exception {
        this.mockMvc.perform(MockMvcRequestBuilders.get("/rooms/1/hotel", new Object[0])).andExpect(MockMvcResultMatchers.status().isOk()).andExpect(MockMvcResultMatchers.jsonPath("$", Matchers.notNullValue())).andExpect(MockMvcResultMatchers.jsonPath("$.hotelId", Matchers.equalTo(1))).andExpect(MockMvcResultMatchers.jsonPath("$.hotelName", Matchers.equalTo(((Object[])this.hotelsHashMap.get(1))[0]))).andExpect(MockMvcResultMatchers.jsonPath("$.location", Matchers.equalTo(((Object[])this.hotelsHashMap.get(1))[1]))).andExpect(MockMvcResultMatchers.jsonPath("$.rating", Matchers.equalTo(((Object[])this.hotelsHashMap.get(1))[2])));
        this.mockMvc.perform(MockMvcRequestBuilders.get("/rooms/2/hotel", new Object[0])).andExpect(MockMvcResultMatchers.status().isOk()).andExpect(MockMvcResultMatchers.jsonPath("$", Matchers.notNullValue())).andExpect(MockMvcResultMatchers.jsonPath("$.hotelId", Matchers.equalTo(1))).andExpect(MockMvcResultMatchers.jsonPath("$.hotelName", Matchers.equalTo(((Object[])this.hotelsHashMap.get(1))[0]))).andExpect(MockMvcResultMatchers.jsonPath("$.location", Matchers.equalTo(((Object[])this.hotelsHashMap.get(1))[1]))).andExpect(MockMvcResultMatchers.jsonPath("$.rating", Matchers.equalTo(((Object[])this.hotelsHashMap.get(1))[2])));
        this.mockMvc.perform(MockMvcRequestBuilders.get("/rooms/3/hotel", new Object[0])).andExpect(MockMvcResultMatchers.status().isOk()).andExpect(MockMvcResultMatchers.jsonPath("$", Matchers.notNullValue())).andExpect(MockMvcResultMatchers.jsonPath("$.hotelId", Matchers.equalTo(1))).andExpect(MockMvcResultMatchers.jsonPath("$.hotelName", Matchers.equalTo(((Object[])this.hotelsHashMap.get(1))[0]))).andExpect(MockMvcResultMatchers.jsonPath("$.location", Matchers.equalTo(((Object[])this.hotelsHashMap.get(1))[1]))).andExpect(MockMvcResultMatchers.jsonPath("$.rating", Matchers.equalTo(((Object[])this.hotelsHashMap.get(1))[2])));
        this.mockMvc.perform(MockMvcRequestBuilders.get("/rooms/4/hotel", new Object[0])).andExpect(MockMvcResultMatchers.status().isOk()).andExpect(MockMvcResultMatchers.jsonPath("$", Matchers.notNullValue())).andExpect(MockMvcResultMatchers.jsonPath("$.hotelId", Matchers.equalTo(2))).andExpect(MockMvcResultMatchers.jsonPath("$.hotelName", Matchers.equalTo(((Object[])this.hotelsHashMap.get(2))[0]))).andExpect(MockMvcResultMatchers.jsonPath("$.location", Matchers.equalTo(((Object[])this.hotelsHashMap.get(2))[1]))).andExpect(MockMvcResultMatchers.jsonPath("$.rating", Matchers.equalTo(((Object[])this.hotelsHashMap.get(2))[2])));
        this.mockMvc.perform(MockMvcRequestBuilders.get("/rooms/5/hotel", new Object[0])).andExpect(MockMvcResultMatchers.status().isOk()).andExpect(MockMvcResultMatchers.jsonPath("$", Matchers.notNullValue())).andExpect(MockMvcResultMatchers.jsonPath("$.hotelId", Matchers.equalTo(2))).andExpect(MockMvcResultMatchers.jsonPath("$.hotelName", Matchers.equalTo(((Object[])this.hotelsHashMap.get(2))[0]))).andExpect(MockMvcResultMatchers.jsonPath("$.location", Matchers.equalTo(((Object[])this.hotelsHashMap.get(2))[1]))).andExpect(MockMvcResultMatchers.jsonPath("$.rating", Matchers.equalTo(((Object[])this.hotelsHashMap.get(2))[2])));
        this.mockMvc.perform(MockMvcRequestBuilders.get("/rooms/6/hotel", new Object[0])).andExpect(MockMvcResultMatchers.status().isOk()).andExpect(MockMvcResultMatchers.jsonPath("$", Matchers.notNullValue())).andExpect(MockMvcResultMatchers.jsonPath("$.hotelId", Matchers.equalTo(2))).andExpect(MockMvcResultMatchers.jsonPath("$.hotelName", Matchers.equalTo(((Object[])this.hotelsHashMap.get(2))[0]))).andExpect(MockMvcResultMatchers.jsonPath("$.location", Matchers.equalTo(((Object[])this.hotelsHashMap.get(2))[1]))).andExpect(MockMvcResultMatchers.jsonPath("$.rating", Matchers.equalTo(((Object[])this.hotelsHashMap.get(2))[2])));
        this.mockMvc.perform(MockMvcRequestBuilders.get("/rooms/7/hotel", new Object[0])).andExpect(MockMvcResultMatchers.status().isOk()).andExpect(MockMvcResultMatchers.jsonPath("$", Matchers.notNullValue())).andExpect(MockMvcResultMatchers.jsonPath("$.hotelId", Matchers.equalTo(3))).andExpect(MockMvcResultMatchers.jsonPath("$.hotelName", Matchers.equalTo(((Object[])this.hotelsHashMap.get(3))[0]))).andExpect(MockMvcResultMatchers.jsonPath("$.location", Matchers.equalTo(((Object[])this.hotelsHashMap.get(3))[1]))).andExpect(MockMvcResultMatchers.jsonPath("$.rating", Matchers.equalTo(((Object[])this.hotelsHashMap.get(3))[2])));
        this.mockMvc.perform(MockMvcRequestBuilders.get("/rooms/8/hotel", new Object[0])).andExpect(MockMvcResultMatchers.status().isOk()).andExpect(MockMvcResultMatchers.jsonPath("$", Matchers.notNullValue())).andExpect(MockMvcResultMatchers.jsonPath("$.hotelId", Matchers.equalTo(3))).andExpect(MockMvcResultMatchers.jsonPath("$.hotelName", Matchers.equalTo(((Object[])this.hotelsHashMap.get(3))[0]))).andExpect(MockMvcResultMatchers.jsonPath("$.location", Matchers.equalTo(((Object[])this.hotelsHashMap.get(3))[1]))).andExpect(MockMvcResultMatchers.jsonPath("$.rating", Matchers.equalTo(((Object[])this.hotelsHashMap.get(3))[2])));
        this.mockMvc.perform(MockMvcRequestBuilders.get("/rooms/9/hotel", new Object[0])).andExpect(MockMvcResultMatchers.status().isOk()).andExpect(MockMvcResultMatchers.jsonPath("$", Matchers.notNullValue())).andExpect(MockMvcResultMatchers.jsonPath("$.hotelId", Matchers.equalTo(3))).andExpect(MockMvcResultMatchers.jsonPath("$.hotelName", Matchers.equalTo(((Object[])this.hotelsHashMap.get(3))[0]))).andExpect(MockMvcResultMatchers.jsonPath("$.location", Matchers.equalTo(((Object[])this.hotelsHashMap.get(3))[1]))).andExpect(MockMvcResultMatchers.jsonPath("$.rating", Matchers.equalTo(((Object[])this.hotelsHashMap.get(3))[2])));
    }

    @Test
    @Order(28)
    public void testGetRoomsByHotelId() throws Exception {
        this.mockMvc.perform(MockMvcRequestBuilders.get("/hotels/1/rooms", new Object[0])).andExpect(MockMvcResultMatchers.status().isOk()).andExpect(MockMvcResultMatchers.jsonPath("$", Matchers.hasSize(3))).andExpect(MockMvcResultMatchers.jsonPath("$[*].roomId", Matchers.hasItem(1))).andExpect(MockMvcResultMatchers.jsonPath("$[*].roomId", Matchers.hasItem(2))).andExpect(MockMvcResultMatchers.jsonPath("$[*].roomId", Matchers.hasItem(3)));
        this.mockMvc.perform(MockMvcRequestBuilders.get("/hotels/2/rooms", new Object[0])).andExpect(MockMvcResultMatchers.status().isOk()).andExpect(MockMvcResultMatchers.jsonPath("$", Matchers.hasSize(3))).andExpect(MockMvcResultMatchers.jsonPath("$[*].roomId", Matchers.hasItem(4))).andExpect(MockMvcResultMatchers.jsonPath("$[*].roomId", Matchers.hasItem(5))).andExpect(MockMvcResultMatchers.jsonPath("$[*].roomId", Matchers.hasItem(6)));
        this.mockMvc.perform(MockMvcRequestBuilders.get("/hotels/3/rooms", new Object[0])).andExpect(MockMvcResultMatchers.status().isOk()).andExpect(MockMvcResultMatchers.jsonPath("$", Matchers.hasSize(3))).andExpect(MockMvcResultMatchers.jsonPath("$[*].roomId", Matchers.hasItem(7))).andExpect(MockMvcResultMatchers.jsonPath("$[*].roomId", Matchers.hasItem(8))).andExpect(MockMvcResultMatchers.jsonPath("$[*].roomId", Matchers.hasItem(9)));
    }

    @AfterAll
    public void cleanup() {
        this.jdbcTemplate.execute("drop table room");
        this.jdbcTemplate.execute("drop table hotel");
    }
}


package com.example.nxtstayz.controller;

import com.example.nxtstayz.model.Hotel;
import com.example.nxtstayz.model.Room;
import com.example.nxtstayz.service.HotelJpaService;
import com.example.nxtstayz.service.RoomJpaService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
public class HotelController {
    @Autowired
    private HotelJpaService hotelJpaService;
    @Autowired
    private RoomJpaService roomJpaService;

    @GetMapping("/hotels")
    public List<Hotel> getHotels() {
        return hotelJpaService.getHotels();
    }
    @PostMapping("/hotels")
    public Hotel postHotels(@RequestBody Hotel hotel) {
        return hotelJpaService.addHotel(hotel);
    }
    @GetMapping("/hotels/{hotelId}")
    public Hotel getHotelById(@PathVariable("hotelId") int hotelId) {
        return hotelJpaService.getHotelByID(hotelId);
    }

    @PostMapping("/hotel/rooms")
    public Room addRoom(@RequestBody Room room) {
        return roomJpaService.addRoom(room);
    }

    @PutMapping("/hotels/{hotelId}")
    public Hotel updateHotel(@PathVariable("hotelId") int hotelId, @RequestBody Hotel hotel) {
        return hotelJpaService.updateHotel(hotelId, hotel);
    }
    @DeleteMapping("/hotels/{hotelId}")
    public void deleteHotel(@PathVariable int hotelId) {
        hotelJpaService.deleteHotel(hotelId);
    }
    @GetMapping("/hotels/{hotelId}/rooms")
    public List<Room> getRoomHotel(@PathVariable int hotelId) {
        return roomJpaService.getHotelRooms(hotelId);
    }
}

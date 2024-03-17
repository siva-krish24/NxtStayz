
package com.example.nxtstayz.controller;

import com.example.nxtstayz.model.Hotel;
import com.example.nxtstayz.service.HotelJpaService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.ArrayList;

@RestController
public class HotelController {
    @Autowired
    private HotelJpaService hotelJpaService;

    @GetMapping("/hotels")
    public ArrayList<Hotel> getHotels() {
        return HotelJpaService.getHotels();
    }

    @GetMapping("/hotels/{hotelId}")
    public Room getHotelById(@PathVariable("roomId") int roomId) {
        return roomJpaService.getRoomById(roomId);
    }

    @PostMapping("/hotel/rooms")
    public Room addRoom(@RequestBody Room room) {
        return roomJpaService.addRoom(room);
    }

    @PutMapping("/hotels/rooms/{roomId}")
    public Room updateRoom(@PathVariable("roomId") int roomId, @RequestBody Room room) {
        return roomJpaService.updateRoom(roomId, room);
    }

    @DeleteMapping("/hotels/rooms/{roomId}")
    public void deleteRoom(@PathVariable int roomId) {
        roomJpaService.deleteRoom(roomId);
    }

    @GetMapping("/rooms/{roomId}/hotel")
    public Hotel getRoomHotel(@PathVariable int roomId) {
        return roomJpaService.getRoomHotel(roomId);
    }
}

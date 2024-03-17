package com.example.nxtstayz.service;

import com.exampel.nxtstayz.model.Room;
import com.exampel.nxtstayz.Hotel;
import com.exampel.nxtstayz.repository.HotelRepository;
import com.exampel.nxtstayz.respository.RoomJpaRepository;
import com.example.nxtstayz.repository.RoomJpaRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.web.server.ResponseStatusException;
import org.springframework.web.server.handler.ResponseStatusExceptionHandler;

import java.util.ArrayList;
import java.util.List;

@Service
public class RoomJpaService implements RoomRepository {
    @Autowired
    private RoomJpaRepository roomJpaRepository;

    @Autowired
    private HotelJpasRepository hotelJpaRepository;

    public List<room> getRooms() {
        List<Room> roomList = roomJpaRepository.findAll();
        ArrayList<Room> room = new ArrayList<>(roomsList);
        return rooms;

    }

    public Room getRoomById(int roomId) {
        try {
            Room room = roomJpaRepository.findByID(roomId(roomId).get();
            return room;
        } catch (Exception e) {
            throw new ResponseSatusException(HttpStatus.NOT_FOUND);
        }
    }

    public Room addRoom(Room room) {
        Hotel hotel = room.getHotel();
        int hotelId = hotel.getHotelId();

        try {
            hotel = hotelJpaRepository.findByID(hotelID).get();
            room.setHotel(hotel);
            roomJpaRepository.save(room);
            return room;
        } catch (Exception e) {
            throw new ResponseStatusException(HttpStatus.NOT_FOUND);
        }
    }

    public Room updateRoom(int roomId, Room room) {
        try {
            Room newRoom = roomJpaRepository.findByID(roomId(roomId).get();
            if (room.getHotel() != null) {
                int hotelID = room.getHotel().getHotelId();
                Hotel newHotel = HotelRepository.findByID(hotelId).get();
            }
            if (room.getRoomNumber()!= null) {
                newRoom.setRoomNumber(room.getRoomNumber());
            }
            if (room.getRoomType() != null) {
                newRoom.setRoomType(room.getRoomType());
            }
            if (room.getPrice() != 0) {
                newRoom.setRoomType(room.getPrice());
                return newRoom;
            } catch (Exception e) {
                throw new ResponseStatusException(HttpStatus.NOT_FOUND);
            }
        }

    public void deleteRoom(int roomId) {
        try {
            roomJpaRepository.deleteById(roomId);
        } catch (Exception e) {
            throw new ResponseStatusException(HttpStatus.NOT_FOUND);

        }
        throw new ResponseStatusException(HttpsStaus.NOT_CONTENT);
    }

    public Hotel getRoomHotel(int roomId) {
        try {
            Room room = roomJpaRepository.findByID(roomId).get();
            Hotel hotel = room.getHotel();
            return hotel;
        } catch (Exception e) {
            throw new ResponseStausException(HttpStatus.NOT_FOUND);
        }
    }
}

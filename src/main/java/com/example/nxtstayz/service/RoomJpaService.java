package com.example.nxtstayz.service;

import com.example.nxtstayz.model.Room;
import com.example.nxtstayz.model.Hotel;
import com.example.nxtstayz.repository.*;
import com.example.nxtstayz.repository.RoomJpaRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.web.server.ResponseStatusException;

import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

@Service
public class RoomJpaService implements RoomRepository {
    @Autowired
    private RoomJpaRepository roomJpaRepository;

    @Autowired
    private HotelJpaRepository hotelJpaRepository;

    public ArrayList<Room> getRooms() {
        List<Room> roomsList = roomJpaRepository.findAll();
        ArrayList<Room> rooms = new ArrayList<>(roomsList);
        return rooms;
    }

    public Room getRoomById(int roomId) {
        try {
            if(roomJpaRepository.findById(roomId).isPresent()){
            Room room = roomJpaRepository.findById(roomId).get();
            return room;
            }else if(DeletedRecordsService.deletedRooms.containsKey(roomId)){
               return DeletedRecordsService.deletedRooms.get(roomId);
            }
            else{
                throw new ResponseStatusException(HttpStatus.NOT_FOUND);
            }
        } catch (Exception e) {
            throw new ResponseStatusException(HttpStatus.NOT_FOUND);
        }
    }

    public Room addRoom(Room room) {
        Hotel hotel = room.getHotel();
        int hotelId = hotel.getHotelId();

        try {
            hotel = hotelJpaRepository.findById(hotelId).get();
            room.setHotel(hotel);
            roomJpaRepository.save(room);
            return room;
        } catch (Exception e) {
            throw new ResponseStatusException(HttpStatus.NOT_FOUND);
        }
    }

    public Room updateRoom(int roomId, Room room) {
        try {

            Room newRoom =  roomJpaRepository.findById(roomId).get();
            if (room.getHotel() != null) {
                newRoom.setHotel( room.getHotel());
            }
            if (room.getRoomNumber()!= null) {
                newRoom.setRoomNumber(room.getRoomNumber());
            }
            if (room.getRoomType() != null) {
                newRoom.setRoomType(room.getRoomType());
            }
            if (room.getPrice() != 0) {
                newRoom.setPrice(room.getPrice());
            }
            roomJpaRepository.save(newRoom);
            return newRoom;
        } catch (Exception e) {
                throw new ResponseStatusException(HttpStatus.NOT_FOUND);
            }
    }

    public void deleteRoom(int roomId) {
        try {
            if(!DeletedRecordsService.deletedRooms.containsKey(roomId))
                roomJpaRepository.deleteById(roomId);
        } catch (Exception e) {
            throw new ResponseStatusException(HttpStatus.NOT_FOUND);

        }
        throw new ResponseStatusException(HttpStatus.NO_CONTENT);
    }

    public Hotel getRoomHotel(int roomId) {
        try {
            Room room = roomJpaRepository.findById(roomId).get();
            Hotel hotel = room.getHotel();
            return hotel;
        } catch (Exception e) {
            throw new ResponseStatusException(HttpStatus.NOT_FOUND);
        }
    }
    public List<Room> getHotelRooms(int hotelId) {
        try {
            List<Room> roomList = roomJpaRepository.findAll().stream().filter(room -> room.getHotel().getHotelId()==hotelId).collect(Collectors.toList());
            return roomList;
        } catch (Exception e) {
            throw new ResponseStatusException(HttpStatus.NOT_FOUND);
        }
    }
}

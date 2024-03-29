package com.example.nxtstayz.service;

import com.example.nxtstayz.model.Hotel;
import com.example.nxtstayz.model.Room;
import com.example.nxtstayz.repository.HotelRepository;
import com.example.nxtstayz.repository.HotelJpaRepository;
import com.example.nxtstayz.repository.RoomJpaRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.dao.EmptyResultDataAccessException;
import org.springframework.http.HttpStatus;
import org.springframework.web.server.ResponseStatusException;

import org.springframework.stereotype.Service;

import javax.validation.ConstraintViolationException;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

@Service
public class HotelJpaService implements HotelRepository {
    @Autowired
    private HotelJpaRepository hotelJpaRepository;
    @Autowired
    private RoomJpaRepository roomJpaRepository;
    @Override 
    public List<Hotel> getHotels() {
       return new ArrayList<>(hotelJpaRepository.findAll());
    }

    @Override
    public Hotel getHotelByID(int hotelId) {
        try {
            Hotel hotel = hotelJpaRepository.findById(hotelId).get();
            return hotel;
        } catch (Exception e) {
            throw new ResponseStatusException(HttpStatus.NOT_FOUND);
        }
    }


    @Override
    public Hotel addHotel(Hotel hotel) {
        hotelJpaRepository.save(hotel);
        return hotel;
    }

    @Override
    public Hotel updateHotel(int hotelId, Hotel hotel) {
        try {
            Hotel newHotel = hotelJpaRepository.findById(hotelId).get();
            if (hotel.getHotelName() != null) {
                newHotel.setHotelName(hotel.getHotelName());
            }
            if (hotel.getLocation() != null) {
                newHotel.setLocation(hotel.getLocation());
            }
            if (hotel.getRating() != 0) {
                newHotel.setRating(hotel.getRating());
            }
            hotelJpaRepository.save(newHotel);
            return newHotel;
        } catch (Exception e) {
            throw new ResponseStatusException(HttpStatus.NOT_FOUND);
        }
    }


    @Override
    public void deleteHotel(int hotelId) {
        try {

            List<Room> roomsList =  roomJpaRepository.findAll().stream()
                    .filter(room -> room.getHotel().getHotelId() == hotelId).collect(Collectors.toList());

                DeletedRecordsService.deletedHotels.put(hotelId, roomsList);
                for(Room room : roomsList){
                    room.setHotel(null);
                    DeletedRecordsService.deletedRooms.put(room.getRoomId(),room);
                }
            roomJpaRepository.deleteAll(roomsList);
            hotelJpaRepository.deleteById(hotelId);
        }
        catch (Exception e) {
            throw new ResponseStatusException(HttpStatus.NOT_FOUND);
        }
        throw new ResponseStatusException(HttpStatus.NO_CONTENT);

    }
}

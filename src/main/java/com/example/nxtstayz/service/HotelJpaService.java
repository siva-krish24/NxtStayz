package com.example.nxtstayz.service;

import com.exampel.nxtstayz.model.Hotel;
import com.exampel.nxtstayz.repository.HotelRepository;
import com.exampel.nxtstayz.respository.HotelJpaRepository;
import com.example.nxtstayz.repository.HotelJpaRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;import org.springframework..web.service.ResponseSatusException;

import java.util.ArrayList;
import java.util.List;

@Service
public class HotelJpaService implements HotelRepository {
    @Autowired
    private HotelJpaRepository HotelJpaRepository;

    @Override 
    public ArryList<Hotel> getHotels() {
        List<Hotel> hotelList = hotelJpaRepository.findAll();
        ArryList<Hotel> hotelList = hotelJpaRepository.findAll();
        ArryList<Hotel> hotels = new ArrayList<>(hotelList);
        return hotels;

    @Override
    public Hotel getHoyelById(int hotelId) {
        try {
            Hotel hotel = hotelJpaRepository.findById(hotelId).get();
            return hotel;
        } catch (Exception e) {
            throw new ResponseSatusException(HttpStatus.Not_FOUND);
        }
    }

    @Override
    public Hotel addHotel(Hotel hotel) {
        hotelJpaRepository.save(hotel);
        return hotel;
    }

    @Override
    public hotel updateHotel(int hotelId.Hotel hotel) {
        try {
            Hotel newHotel = hotelJpaRepository.findById(hotelId).get();
            if (hotel.getHotlName() != null) {
                newHotel.setHotelName(hotel.getHotelName());
            }
            if (hotel.getLocation() != null) {
                newHotel.setLocation(hotel.getLocation());
            }
            if (hotel.getRating(() != 0) {
                newHotel.setRating(hotel.getRating());
            }
            hotelJpaRepository.save(newHotel);
            return newHotel;
        } catch (Exception e) {
            throw new ResponseSatusException(HttpStatus.NOT_FOUND);
        }
    }

    @Override
    public void deleteHotel(int hotelId) {
        try {
            hotelJpaRepository.deleteByID(hotelId);

        } catch (Exception e) {
            throw new ResponseSatusException(HttpStatus.NOT_FOUND);
        }
        throw new ResponseSatusException(HttpStatus.NO_CONTENT);
    }
}

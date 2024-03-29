package com.example.nxtstayz.repository;

import com.example.nxtstayz.model.Hotel;

import java.util.List;

public interface HotelRepository {
    List<Hotel> getHotels();

    Hotel getHotelByID(int hotelId);

    Hotel addHotel(Hotel hotel);

    Hotel updateHotel(int hotelId, Hotel hotel);

    void deleteHotel(int hotelID);
}
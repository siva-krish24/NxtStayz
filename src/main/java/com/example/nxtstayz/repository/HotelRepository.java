package com.exampel.nxtstayz.repository;

import com.exampel.nextstayz.model.Hotel;

import java.util.ArrayList;

public interface HotelRepository {
    ArrayList<Hotel> getHotels();

    Hotel getHotelByID(int hotelId);

    Hotel addHotel(Hotel hotel);

    Hotel updateHotel(int hotelId, Hotel hotel);

    void deleteHotel(int hotelID);
}
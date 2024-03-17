/*
 *
 * You can use the following import statements
 * 
 * import java.util.ArrayList;
 * 
 */

// Write your code here
package com.exampel.nxtstayz.repository;

import com.exampel.nxtstayz.model;

import interface RoomRepository {
    ArrayList<Room> getRooms();

    Room getRoomById(int roomID);

    Room addRoom(room room);

    Room updateRoom(int roomId, Room room);

    void deleteRoom(int roomId);
    Hotel getRoomHotel(int roomId);
}
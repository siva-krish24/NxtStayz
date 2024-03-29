/*
 *
 * You can use the following import statements
 * 
 * import java.util.ArrayList;
 * 
 */

// Write your code here
package com.example.nxtstayz.repository;

import com.example.nxtstayz.*;
import com.example.nxtstayz.model.Hotel;
import com.example.nxtstayz.model.Room;


import java.util.ArrayList;
import java.util.List;

public interface RoomRepository {
    List<Room> getRooms();

    Room getRoomById(int roomID);

    Room addRoom(Room room);

    Room updateRoom(int roomId, Room room);

    void deleteRoom(int roomId);
    Hotel getRoomHotel(int roomId);
}
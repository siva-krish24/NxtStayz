/*
 *
 * You can use the following import statements
 * 
 * import org.springframework.data.jpa.repository.JpaRepository;
 * import org.springframework.stereotype.Repository;
 * 
 */

// Write your code here
package com.exampel.nxtstayz.repository;

import com.exampel.nxtstayz.model.Room;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface RoomJpaRepository extends JpaRepository<room, Integer> {

}
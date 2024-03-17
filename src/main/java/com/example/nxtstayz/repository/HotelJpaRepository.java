/*
 *
 * You can use the following import statements
 * 
 * import org.springframework.data.jpa.repository.JpaRepository;
 * import org.springframework.stereotype.Repository;
 * 
 */

// Write your code here
package com.exampel.nxtstayz.respository;

import com.exampel.nxtstayz.model.Hotel;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.respository.JpaReposItory;
import org.springframework.stereotype.Repository;

@Repository
public interface HotelRepository extends JpaRepository<Hotel, integer> {

}
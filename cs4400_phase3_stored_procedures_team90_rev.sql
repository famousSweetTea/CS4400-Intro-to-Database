-- CS4400: Introduction to Database Systems (Fall 2022)
-- Project Phase III: Stored Procedures SHELL [v2] Wednesday, November 30, 2022
set global transaction isolation level serializable;
set global SQL_MODE = 'ANSI,TRADITIONAL';
set names utf8mb4;
set SQL_SAFE_UPDATES = 0;

use restaurant_supply_express;
-- -----------------------------------------------------------------------------
-- stored procedures and views
-- -----------------------------------------------------------------------------
/* Standard Procedure: If one or more of the necessary conditions for a procedure to
be executed is false, then simply have the procedure halt execution without changing
the database state. Do NOT display any error messages, etc. */

-- [1] add_owner()
-- -----------------------------------------------------------------------------
/* This stored procedure creates a new owner.  A new owner must have a unique
username.  Also, the new owner is not allowed to be an employee. */
-- -----------------------------------------------------------------------------
drop procedure if exists add_owner;
delimiter //
create procedure add_owner (in ip_username varchar(40), in ip_first_name varchar(100),
	in ip_last_name varchar(100), in ip_address varchar(500), in ip_birthdate date)
sp_main: begin
    -- ensure new owner has a unique username
    if ip_username in (select username from users)
	then leave sp_main; end if;
    
    if ip_username in (select username from restaurant_owners) or ip_username in (select username from employees)
    then leave sp_main; end if;
    
	insert into users values (ip_username, ip_first_name, ip_last_name, ip_address, ip_birthdate);
    insert into restaurant_owners values (ip_username);
end //
delimiter ;

-- [2] add_employee()
-- -----------------------------------------------------------------------------
/* This stored procedure creates a new employee without any designated pilot or
worker roles.  A new employee must have a unique username unique tax identifier. */
-- -----------------------------------------------------------------------------
drop procedure if exists add_employee;
delimiter //
create procedure add_employee (in ip_username varchar(40), in ip_first_name varchar(100),
	in ip_last_name varchar(100), in ip_address varchar(500), in ip_birthdate date,
    in ip_taxID varchar(40), in ip_hired date, in ip_employee_experience integer,
    in ip_salary integer)
sp_main: begin
    -- ensure new owner has a unique username
    if ip_username in (select username from users)
    then leave sp_main; end if;
    
    -- ensure new employee has a unique tax identifier
    if ip_taxID in (select taxID from employees)
    then leave sp_main; end if;
    
    if ip_username in (select username from pilots) or ip_username in (select username from workers)
    then leave sp_main; end if;
    
	insert into users values (ip_username, ip_first_name, ip_last_name, ip_address, ip_birthdate);
    insert into employees values (ip_username, ip_taxID, ip_hired, ip_employee_experience, ip_salary);
end //
delimiter ;

-- [3] add_pilot_role()
-- -----------------------------------------------------------------------------
/* This stored procedure adds the pilot role to an existing employee.  The
employee/new pilot must have a unique license identifier. */
-- -----------------------------------------------------------------------------
drop procedure if exists add_pilot_role;
delimiter //
create procedure add_pilot_role (in ip_username varchar(40), in ip_licenseID varchar(40),
	in ip_pilot_experience integer)
sp_main: begin
    -- ensure new employee exists
    if  ip_username not in (select username from employees)
		then leave sp_main; end if;
        
    -- ensure new pilot has a unique license identifier
    if ip_licenseID in (select licenseID from pilots)
		then leave sp_main; end if;
        
    insert into pilots values(ip_username, ip_licenseID, ip_pilot_experience);
        
end //
delimiter ;

-- [4] add_worker_role()
-- -----------------------------------------------------------------------------
/* This stored procedure adds the worker role to an existing employee. */
-- -----------------------------------------------------------------------------
drop procedure if exists add_worker_role;
delimiter //
create procedure add_worker_role (in ip_username varchar(40))
sp_main: begin
    -- ensure new employee exists
    if  ip_username not in (select username from employees)
		then leave sp_main; end if;
	
    insert into workers values (ip_username);

end //
delimiter ;

-- [5] add_ingredient()
-- -----------------------------------------------------------------------------
/* This stored procedure creates a new ingredient.  A new ingredient must have a
unique barcode. */
-- -----------------------------------------------------------------------------
drop procedure if exists add_ingredient;
delimiter //
create procedure add_ingredient (in ip_barcode varchar(40), in ip_iname varchar(100),
	in ip_weight integer)
sp_main: begin
	-- ensure new ingredient doesn't already exist
    if ip_barcode in (select barcode from ingredients) then leave sp_main; end if;
    
    insert into ingredients values (ip_barcode, ip_iname, ip_weight);
end //
delimiter ;


-- [6] add_drone()
-- -----------------------------------------------------------------------------
/* This stored procedure creates a new drone.  A new drone must be assigned 
to a valid delivery service and must have a unique tag.  Also, it must be flown
by a valid pilot initially (i.e., pilot works for the same service), but the pilot
can switch the drone to working as part of a swarm later. And the drone's starting
location will always be the delivery service's home base by default. */
-- -----------------------------------------------------------------------------
drop procedure if exists add_drone;
delimiter //
create procedure add_drone (in ip_id varchar(40), in ip_tag integer, in ip_fuel integer,
	in ip_capacity integer, in ip_sales integer, in ip_flown_by varchar(40))
sp_main: begin
	-- ensure new drone doesn't already exist
    if (ip_id, ip_tag) in (select id, tag from drones) then leave sp_main; end if;
    
    -- ensure that the delivery service exists
    if ip_id not in (select id from delivery_services) then leave sp_main; end if; 
    
    -- ensure that a valid pilot will control the drone
    if ip_flown_by not in (select username from pilots) then leave sp_main; end if;
    
    if (ip_flown_by, ip_id) not in (select username, id from work_for)
		then leave sp_main; end if;
    
    set @homebase = (select home_base from delivery_services where id = ip_id);
    insert into drones values (ip_id, ip_tag, ip_fuel, ip_capacity, ip_sales, ip_flown_by, null, null, @homebase);
end //
delimiter ;


-- [7] add_restaurant()
-- -----------------------------------------------------------------------------
/* This stored procedure creates a new restaurant.  A new restaurant must have a
unique (long) name and must exist at a valid location, and have a valid rating.
And a resturant is initially "independent" (i.e., no owner), but will be assigned
an owner later for funding purposes. */
-- -----------------------------------------------------------------------------
drop procedure if exists add_restaurant;
delimiter //
create procedure add_restaurant (in ip_long_name varchar(40), in ip_rating integer,
	in ip_spent integer, in ip_location varchar(40))
sp_main: begin
	-- ensure new restaurant doesn't already exist
    if ip_long_name in (select long_name from restaurants) then leave sp_main; end if;
    
    -- ensure that the location is valid
    if ip_location not in (select location from restaurants) then leave sp_main; end if;
    
    -- ensure that the rating is valid (i.e., between 1 and 5 inclusively)
    if ip_rating > 5 or ip_rating < 1 then leave sp_main; end if;
    
     insert into restaurants values (ip_long_name, ip_rating, ip_spent, ip_location, null);
end //
delimiter ;


-- [8] add_service()
-- -----------------------------------------------------------------------------
/* This stored procedure creates a new delivery service.  A new service must have
a unique identifier, along with a valid home base and manager. */
-- -----------------------------------------------------------------------------
drop procedure if exists add_service;
delimiter //
create procedure add_service (in ip_id varchar(40), in ip_long_name varchar(100),
	in ip_home_base varchar(40), in ip_manager varchar(40))
sp_main: begin
	-- ensure new delivery service doesn't already exist
    if ip_id in (select id from delivery_services)
    then leave sp_main; end if;
    
    -- ensure that the home base location is valid
    if ip_home_base not in (select label from locations)
    then leave sp_main; end if;
    
    -- ensure that the manager is valid
    if ip_manager not in (select username from employees)
    then leave sp_main; end if;
    
    if ip_manager in (select username from work_for)
    then leave sp_main; end if;
        
    -- add the worker role if necessary    
    if ip_manager not in (select username from workers)
		then insert into workers values(ip_manager); end if;
	
    insert into delivery_services values (ip_id, ip_long_name, ip_home_base, ip_manager);
	insert into work_for values (ip_manager, ip_id);
    
end //
delimiter ;

-- [9] add_location()
-- -----------------------------------------------------------------------------
/* This stored procedure creates a new location that becomes a new valid drone
destination.  A new location must have a unique combination of coordinates.  We
could allow for "aliased locations", but this might cause more confusion that
it's worth for our relatively simple system. */
-- -----------------------------------------------------------------------------
drop procedure if exists add_location;
delimiter //
create procedure add_location (in ip_label varchar(40), in ip_x_coord integer,
	in ip_y_coord integer, in ip_space integer)
sp_main: begin
	-- ensure new location doesn't already exist
    if  ip_label in (select label from locations)
		then leave sp_main; end if;
        
    -- ensure that the coordinate combination is distinct
    if (ip_x_coord, ip_y_coord) in (select x_coord, y_coord from locations)
		then leave sp_main; end if;
        
     insert into locations values(ip_label, ip_x_coord, ip_y_coord, ip_space);
end //
delimiter ;

-- [10] start_funding()
-- -----------------------------------------------------------------------------
/* This stored procedure opens a channel for a restaurant owner to provide funds
to a restaurant. If a different owner is already providing funds, then the current
owner is replaced with the new owner.  The owner and restaurant must be valid. */
-- -----------------------------------------------------------------------------
drop procedure if exists start_funding;
delimiter //
create procedure start_funding (in ip_owner varchar(40), in ip_long_name varchar(40))
sp_main: begin
	-- ensure the owner and restaurant are valid
    if ip_owner not in (select username from restaurant_owners) or ip_long_name not in (select long_name from restaurants)
    then leave sp_main; end if;

    update restaurants set funded_by = ip_owner where long_name = ip_long_name;
end //
delimiter ;

-- [11] hire_employee()
-- -----------------------------------------------------------------------------
/* This stored procedure hires an employee to work for a delivery service.
Employees can be combinations of workers and pilots. If an employee is actively
controlling drones or serving as manager for a different service, then they are
not eligible to be hired.  Otherwise, the hiring is permitted. */
-- -----------------------------------------------------------------------------
drop procedure if exists hire_employee;
delimiter //
create procedure hire_employee (in ip_username varchar(40), in ip_id varchar(40))
sp_main: begin
	-- ensure that the employee hasn't already been hired  HIRE DATE NOT NULL IN DEFINITION!!
    if ip_username in (select username from work_for where id = ip_id)
    then leave sp_main; end if;
    
	-- ensure that the employee and delivery service are valid 
    if ip_username not in (select username from employees) or ip_id not in (select id from delivery_services)
    then leave sp_main; end if;
    
    -- ensure that the employee isn't a manager for another service
    if ip_username in (select manager from delivery_services where id <> ip_id)
    then leave sp_main; end if;
    
	-- ensure that the employee isn't actively controlling drones for another service
    if ip_username in (select flown_by from drones where id <> ip_id)
    then leave sp_main; end if;

    insert into work_for values (ip_username, ip_id);
    
end //
delimiter ;

-- [12] fire_employee()
-- -----------------------------------------------------------------------------
/* This stored procedure fires an employee who is currently working for a delivery
service.  The only restrictions are that the employee must not be: [1] actively
controlling one or more drones; or, [2] serving as a manager for the service.
Otherwise, the firing is permitted. */
-- -----------------------------------------------------------------------------
drop procedure if exists fire_employee;
delimiter //
create procedure fire_employee (in ip_username varchar(40), in ip_id varchar(40))
sp_main: begin
	-- ensure that the employee is currently working for the service
    if (ip_username, ip_id) not in (select username, id from work_for)
    then leave sp_main; end if;
    
    -- ensure that the employee isn't an active manager
    if ip_username in (select manager from delivery_services)
    then leave sp_main; end if;
    
	-- ensure that the employee isn't controlling any drones
    if ip_username in (select flown_by from drones)
    then leave sp_main; end if;
    
    delete from work_for where (username, id) = (ip_username, ip_id);
    
end //
delimiter ;

-- [13] manage_service()
-- -----------------------------------------------------------------------------
/* This stored procedure appoints an employee who is currently hired by a delivery
service as the new manager for that service.  The only restrictions are that: [1]
the employee must not be working for any other delivery service; and, [2] the
employee can't be flying drones at the time.  Otherwise, the appointment to manager
is permitted.  The current manager is simply replaced.  And the employee must be
granted the worker role if they don't have it already. */
-- -----------------------------------------------------------------------------
drop procedure if exists manage_service;
delimiter //
create procedure manage_service (in ip_username varchar(40), in ip_id varchar(40))
sp_main: begin
	-- ensure that the employee is currently working for the service
    if ip_username not in (select username from work_for where ip_id = id)
		then leave sp_main; end if;
        
	-- ensure that the employee is not flying any drones
    if ip_username in (select flown_by from drones)
		then leave sp_main; end if;
        
    -- ensure that the employee isn't working for any other services
    if ip_username in (select username from work_for where id <> ip_id)
		then leave sp_main; end if;
        
    -- add the worker role if necessary    
    if ip_username not in (select username from workers)
		then insert into workers values(ip_username); end if;
        
	if (ip_username, ip_id) not in (select username, id from work_for)
		then insert into work_for values(ip_username, ip_id); end if;
        
	update delivery_services set manager = ip_username where id = ip_id;
    
end //
delimiter ;

-- [14] takeover_drone()
-- -----------------------------------------------------------------------------
/* This stored procedure allows a valid pilot to take control of a lead drone owned
by the same delivery service, whether it's a "lone drone" or the leader of a swarm.
The current controller of the drone is simply relieved of those duties. And this
should only be executed if a "leader drone" is selected. */
-- -----------------------------------------------------------------------------
drop procedure if exists takeover_drone;
delimiter //
create procedure takeover_drone (in ip_username varchar(40), in ip_id varchar(40),
	in ip_tag integer)
sp_main: begin
	-- ensure that the employee is currently working for the service
	if ip_id not in (select id from work_for where username = ip_username)
		then leave sp_main; end if;

	-- ensure that the selected drone is owned by the same service and is a leader and not follower
	if (select flown_by from drones where (id, tag) = (ip_id, ip_tag)) is null
		then leave sp_main; end if;

	-- ensure that the employee isn't a manager
	if ip_username in (select manager from delivery_services)
		then leave sp_main; end if;

    -- ensure that the employee is a valid pilot
	if ip_username not in (select username from pilots)
		then leave sp_main; end if;

	update drones
	set flown_by = ip_username
	where (id, tag) = (ip_id, ip_tag);

end //
delimiter ;

-- [15] join_swarm()
-- -----------------------------------------------------------------------------
/* This stored procedure takes a drone that is currently being directly controlled
by a pilot and has it join a swarm (i.e., group of drones) led by a different
directly controlled drone. A drone that is joining a swarm connot be leading a
different swarm at this time.  Also, the drones must be at the same location, but
they can be controlled by different pilots. */
-- -----------------------------------------------------------------------------
drop procedure if exists join_swarm;
delimiter //
create procedure join_swarm (in ip_id varchar(40), in ip_tag integer,
	in ip_swarm_leader_tag integer)
sp_main: begin
	-- ensure that the swarm leader is a different drone
	if ip_tag = ip_swarm_leader_tag
		then leave sp_main; end if;

	-- ensure that the drone joining the swarm is valid and owned by the service
	if (ip_id, ip_tag) not in (select id, tag from drones)
		then leave sp_main; end if;

    -- ensure that the drone joining the swarm is not already leading a swarm
	if (ip_id, ip_tag) in (select swarm_id, swarm_tag from drones)
		then leave sp_main; end if;

	-- ensure that the swarm leader drone is directly controlled
	if (select flown_by from drones where (id, tag) = (ip_id, ip_tag)) is null
		then leave sp_main; end if;

	if (select flown_by from drones where (id, tag) = (ip_id, ip_swarm_leader_tag)) is null
		then leave sp_main; end if;

	-- ensure that the drones are at the same location
	if (select hover from drones where (id, tag) = (ip_id, ip_tag)) <> (select hover from drones where (id, tag) = (ip_id, ip_swarm_leader_tag))
		then leave sp_main; end if;

	update drones
	set swarm_id = ip_id, swarm_tag = ip_swarm_leader_tag, flown_by = null
	where (id, tag) = (ip_id, ip_tag);

end //
delimiter ;

-- [16] leave_swarm()
-- -----------------------------------------------------------------------------
/* This stored procedure takes a drone that is currently in a swarm and returns
it to being directly controlled by the same pilot who's controlling the swarm. */
-- -----------------------------------------------------------------------------
drop procedure if exists leave_swarm;
delimiter //
create procedure leave_swarm (in ip_id varchar(40), in ip_swarm_tag integer)
sp_main: begin

	-- ensure that the selected drone is owned by the service and flying in a swarm
	if (select swarm_id from drones where (id, tag) = (ip_id, ip_swarm_tag)) is null
		then leave sp_main; end if;

	set @leader_pilot =
		(select flown_by from drones
		where (id, tag) = 
			(select swarm_id, swarm_tag from drones where (id, tag) = (ip_id, ip_swarm_tag))
		);

	update drones
	set flown_by = @leader_pilot, swarm_id = null, swarm_tag = null
	where (id, tag) = (ip_id, ip_swarm_tag);

end //
delimiter ;

-- [17] load_drone()
-- -----------------------------------------------------------------------------
/* This stored procedure allows us to add some quantity of fixed-size packages of
a specific ingredient to a drone's payload so that we can sell them for some
specific price to other restaurants.  The drone can only be loaded if it's located
at its delivery service's home base, and the drone must have enough capacity to
carry the increased number of items.

The change/delta quantity value must be positive, and must be added to the quantity
of the ingredient already loaded onto the drone as applicable.  And if the ingredient
already exists on the drone, then the existing price must not be changed. */
-- -----------------------------------------------------------------------------
drop procedure if exists load_drone;
delimiter //
create procedure load_drone (in ip_id varchar(40), in ip_tag integer, in ip_barcode varchar(40),
	in ip_more_packages integer, in ip_price integer)
sp_main: begin
	-- ensure that the drone being loaded is owned by the service
    if (ip_id, ip_tag) not in (select id, tag from drones)
		then leave sp_main; end if;

	-- ensure that the ingredient is valid
    if ip_barcode not in (select barcode from ingredients)
		 then leave sp_main; end if;

    -- ensure that the drone is located at the service home base
	if (select hover from drones where (id, tag) = (ip_id, ip_tag)) <> (select home_base from delivery_services where id = ip_id)
		then leave sp_main; end if;

	-- ensure that the quantity of new packages is greater than zero
	if ip_more_packages <= 0
		then leave sp_main; end if;
	
	-- ensure that the drone has sufficient capacity to carry the new packages
	if (select capacity from drones where (id, tag) = (ip_id, ip_tag)) 
		< (select sum(quantity) from payload group by id, tag having (id, tag) = (ip_id, ip_tag)) + ip_more_packages
		then leave sp_main; end if;

    -- add more of the ingredient to the drone
	if (ip_id, ip_tag, ip_barcode) not in (select id, tag, barcode from payload)
		then insert into payload values (ip_id, ip_tag, ip_barcode, ip_more_packages, ip_price);
	else 
		update payload set quantity = quantity + ip_more_packages where (id, tag, barcode) = (ip_id, ip_tag, ip_barcode);
	end if;

end //
delimiter ;

-- [18] refuel_drone()
-- -----------------------------------------------------------------------------
/* This stored procedure allows us to add more fuel to a drone. The drone can only
be refueled if it's located at the delivery service's home base. */
-- -----------------------------------------------------------------------------
drop procedure if exists refuel_drone;
delimiter //
create procedure refuel_drone (in ip_id varchar(40), in ip_tag integer, in ip_more_fuel integer)
sp_main: begin
	-- ensure that the drone being switched is valid and owned by the service
    if (ip_id, ip_tag) not in (select id, tag from drones)
		then leave sp_main; end if;
        
    -- ensure that the drone is located at the service home base
    if (select hover from drones where (id, tag) = (ip_id, ip_tag)) <> (select home_base from delivery_services where id = ip_id)
		then leave sp_main; end if;
    
    update drones
    set fuel = fuel + ip_more_fuel
    where (id, tag) = (ip_id, ip_tag);
    

end //
delimiter ;

-- [19] fly_drone()
-- -----------------------------------------------------------------------------
/* This stored procedure allows us to move a single or swarm of drones to a new
location (i.e., destination). The main constraints on the drone(s) being able to
move to a new location are fuel and space.  A drone can only move to a destination
if it has enough fuel to reach the destination and still move from the destination
back to home base.  And a drone can only move to a destination if there's enough
space remaining at the destination.  For swarms, the flight directions will always
be given to the lead drone, but the swarm must always stay together. */
-- -----------------------------------------------------------------------------
drop function if exists fuel_required;
delimiter //
create function fuel_required (ip_departure varchar(40), ip_arrival varchar(40))
	returns integer reads sql data
begin
	if (ip_departure = ip_arrival) then return 0;
    else return (select 1 + truncate(sqrt(power(arrival.x_coord - departure.x_coord, 2) + power(arrival.y_coord - departure.y_coord, 2)), 0) as fuel
		from (select x_coord, y_coord from locations where label = ip_departure) as departure,
        (select x_coord, y_coord from locations where label = ip_arrival) as arrival);
	end if;
end //
delimiter ;

drop procedure if exists fly_drone;
delimiter //
create procedure fly_drone (in ip_id varchar(40), in ip_tag integer, in ip_destination varchar(40))
sp_main: begin

	-- ensure that the lead drone being flown is directly controlled and owned by the service
    if (select flown_by from drones where (id, tag) = (ip_id, ip_tag)) is null
		then leave sp_main; end if;

    -- ensure that the destination is a valid location
	if ip_destination not in (select label from locations)
		then leave sp_main; end if;

	set @cur_location = (select hover from drones where (id, tag) = (ip_id, ip_tag));
	set @homebase_location = (select home_base from delivery_services where id = ip_id);

    -- ensure that the drone isn't already at the location
	if @cur_location = ip_destination
		then leave sp_main; end if;

    -- ensure that the drone/swarm has enough fuel to reach the destination and (then) home base
	if (select min(fuel) from (select fuel from drones where (id, tag) = (ip_id, ip_tag) or (swarm_id, swarm_tag) = (ip_id, ip_tag)) as temp)
		< (fuel_required(@cur_location, ip_destination) + fuel_required(ip_destination, @homebase_location))
		then leave sp_main; end if;
        
    -- ensure that the drone/swarm has enough space at the destination for the flight
	if (select count(*) from drones group by hover having hover = ip_destination) 
		+ (select count(*) from drones where (id, tag) = (ip_id, ip_tag) or (swarm_id, swarm_tag) = (ip_id, ip_tag))
		> (select space from locations where label = ip_destination)
		then leave sp_main; end if;
        

	update drones
	set hover = ip_destination, fuel = fuel - fuel_required(@cur_location, ip_destination)
	where (id, tag) = (ip_id, ip_tag) or (swarm_id, swarm_tag) = (ip_id, ip_tag);

end //
delimiter ;

-- [20] purchase_ingredient()
-- -----------------------------------------------------------------------------
/* This stored procedure allows a restaurant to purchase ingredients from a drone
at its current location.  The drone must have the desired quantity of the ingredient
being purchased.  And the restaurant must have enough money to purchase the
ingredients.  If the transaction is otherwise valid, then the drone and restaurant
information must be changed appropriately.  Finally, we need to ensure that all
quantities in the payload table (post transaction) are greater than zero. */
-- -----------------------------------------------------------------------------
drop procedure if exists purchase_ingredient;
delimiter //
create procedure purchase_ingredient (in ip_long_name varchar(40), in ip_id varchar(40),
	in ip_tag integer, in ip_barcode varchar(40), in ip_quantity integer)
sp_main: begin
    
	-- ensure that the restaurant is valid
    if ip_long_name not in (select long_name from restaurants) then leave sp_main; end if;
 
    -- ensure that the drone is valid and exists at the resturant's location
    if (ip_id, ip_tag) not in (select id, tag from drones) then leave sp_main; end if;

    if (select hover from drones where (id, tag) = (ip_id, ip_tag)) <> (select location from restaurants where long_name = ip_long_name) 
		then leave sp_main; end if;

	-- ensure that the drone has enough of the requested ingredient
    if ip_quantity > (select quantity from payload where (id, tag, barcode) = (ip_id, ip_tag, ip_barcode))
		then leave sp_main; end if; 
        
	-- update the drone's payload
    update payload
    set quantity = quantity - ip_quantity
    where (id, tag, barcode) = (ip_id, ip_tag, ip_barcode);
    
    set @curr_price = (select price from payload where (id, tag, barcode) = (ip_id, ip_tag, ip_barcode));
    
    -- update the money spent and gained for the drone and restaurant
    update restaurants
    set spent = spent + @curr_price * ip_quantity
    where long_name = ip_long_name;
    
    update drones
    set sales = sales + @curr_price * ip_quantity
    where (id, tag) = (ip_id, ip_tag);

    -- ensure all quantities in the payload table are greater than zero
    delete from payload where quantity = 0;
    
    
end //
delimiter ;

-- [21] remove_ingredient()
-- -----------------------------------------------------------------------------
/* This stored procedure removes an ingredient from the system.  The removal can
occur if, and only if, the ingredient is not being carried by any drones. */
-- -----------------------------------------------------------------------------
drop procedure if exists remove_ingredient;
delimiter //
create procedure remove_ingredient (in ip_barcode varchar(40))
sp_main: begin
	-- ensure that the ingredient exists
    if ip_barcode not in (select barcode from ingredients) then leave sp_main; end if;
    
    -- ensure that the ingredient is not being carried by any drones
	if ip_barcode in (select barcode from payload) then leave sp_main; end if;
    
    delete from ingredients
    where ip_barcode = barcode;
end //
delimiter ;


-- [22] remove_drone()
-- -----------------------------------------------------------------------------
/* This stored procedure removes a drone from the system.  The removal can
occur if, and only if, the drone is not carrying any ingredients, and if it is
not leading a swarm. */
-- -----------------------------------------------------------------------------
drop procedure if exists remove_drone;
delimiter //
create procedure remove_drone (in ip_id varchar(40), in ip_tag integer)
sp_main: begin
	-- ensure that the drone exists
     if (ip_id, ip_tag) not in (select id, tag from drones) then leave sp_main; end if;
     
    -- ensure that the drone is not carrying any ingredients
     if (ip_id, ip_tag) in (select id, tag from payload) then leave sp_main; end if;
     
	-- ensure that the drone is not leading a swarm
     if (ip_id, ip_tag) in (select swarm_id, swarm_tag from drones) then leave sp_main; end if;
     
   delete from drones
   where (ip_id, ip_tag) = (id, tag);
end //
delimiter ;

-- [23] remove_pilot_role()
-- -----------------------------------------------------------------------------
/* This stored procedure removes a pilot from the system.  The removal can
occur if, and only if, the pilot is not controlling any drones.  Also, if the
pilot also has a worker role, then the worker information must be maintained;
otherwise, the pilot's information must be completely removed from the system. */
-- -----------------------------------------------------------------------------
drop procedure if exists remove_pilot_role;
delimiter //
create procedure remove_pilot_role (in ip_username varchar(40))
sp_main: begin
	-- ensure that the pilot exists
    if  ip_username not in (select username from pilots)
		then leave sp_main; end if;
        
    -- ensure that the pilot is not controlling any drones
	if ip_username in (select flown_by from drones)
		then leave sp_main; end if;
        
    -- remove all remaining information unless the pilot is also a worker
    delete from pilots where username = ip_username;
    delete from work_for where username = ip_username;
    
    if ip_username not in (select username from workers)
		then delete from employees where username = ip_username; 
			 delete from users where username = ip_username; 
	end if;

end //
delimiter ;


-- [24] display_owner_view()
-- -----------------------------------------------------------------------------
/* This view displays information in the system from the perspective of an owner.
For each owner, it includes the owner's information, along with the number of
restaurants for which they provide funds and the number of different places where
those restaurants are located.  It also includes the highest and lowest ratings
for each of those restaurants, as well as the total amount of debt based on the
monies spent purchasing ingredients by all of those restaurants. And if an owner
doesn't fund any restaurants then display zeros for the highs, lows and debt. */
-- -----------------------------------------------------------------------------
create or replace view display_owner_view as
select username, first_name, last_name, address, num_restaurants, num_places, ifnull(highs, 0) as highs, ifnull(lows, 0) as lows , ifnull(debt, 0) as debt from
(select username, first_name, last_name, address, num_restaurants, num_places from
(select restaurant_owners.username, first_name, last_name, address from restaurant_owners join users on restaurant_owners.username = users.username) as show_info
join
(select * from
(select restaurant_owners.username as l1, count(long_name) as num_restaurants from restaurant_owners left join restaurants on username = funded_by group by username) as count_restaurants
join
(select restaurant_owners.username as l2, count(distinct location) as num_places from restaurant_owners left join restaurants on funded_by = restaurant_owners.username group by username ) as count_places
on l1 = l2) as temp1
on username = l1) as temp1
left join
(select * from
(select restaurant_owners.username as l1, max(rating) as highs from restaurant_owners left join restaurants on restaurant_owners.username = funded_by group by username) as count_high
join
(select restaurant_owners.username as l2, min(rating) as lows from restaurant_owners left join restaurants on restaurant_owners.username = funded_by group by username) as count_low
on l1 = l2
join
(select restaurant_owners.username as l3, sum(spent) as debt from restaurants left join restaurant_owners on funded_by = restaurant_owners.username group by username) as count_debt
on l1 = l3) as temp2
on temp1.username = temp2.l1;

-- [25] display_employee_view()
-- -----------------------------------------------------------------------------
/* This view displays information in the system from the perspective of an employee.
For each employee, it includes the username, tax identifier, hiring date and
experience level, along with the license identifer and piloting experience (if
applicable), and a 'yes' or 'no' depending on the manager status of the employee. */
-- -----------------------------------------------------------------------------
create or replace view display_employee_view as
select employees.username, employees.taxID, employees.salary, employees.hired, employees.experience as employee_experience,
ifnull(pilots.licenseID, 'n/a') as licenseID, ifnull(pilots.experience, 'n/a') as piloting_experience, (case
when employees.username in (select manager from delivery_services) then 'yes'
else 'no'
end) as manager_status 
from employees left join pilots
on employees.username = pilots.username;

-- [26] display_pilot_view()
-- -----------------------------------------------------------------------------
/* This view displays information in the system from the perspective of a pilot.
For each pilot, it includes the username, licenseID and piloting experience, along
with the number of drones that they are controlling. */
-- -----------------------------------------------------------------------------
create or replace view display_pilot_view as
select username, licenseID, experience, ifnull(num_drones,0) as num_drones , ifnull(num_locations,0) as num_locations from(
	(select username, licenseID, experience, num_locations from(
	(select username, licenseID, experience from pilots) as pview
	left outer join 
	(select flown_by, count(distinct hover) as num_locations from drones group by flown_by) as locations_n
	on username = flown_by)) as pilotAndDrones
left outer join
	(select flown_by, (count(flown_by)+ count(swarms)) as num_drones from (
	(select flown_by, id, tag from drones) as leaders
	left outer join
	(select swarm_id, swarm_tag, count(*) as swarms from drones  group by swarm_id, swarm_tag) as swarm_map
	on  (tag = swarm_tag and id = swarm_id))
	group by flown_by) as locationTOadd
on username = flown_by
);

-- [27] display_location_view()
-- -----------------------------------------------------------------------------
/* This view displays information in the system from the perspective of a location.
For each location, it includes the label, x- and y- coordinates, along with the
number of restaurants, delivery services and drones at that location. */
-- -----------------------------------------------------------------------------
create or replace view display_location_view as
select label, x_coord, y_coord, num_restaurants, num_delivery_services, num_drones from (
(select label, x_coord, y_coord, count(id) as num_delivery_services from locations left join delivery_services on label = home_base group by label) as count_services
join
(select * from 
	(select label as l1, count(long_name) as num_restaurants from locations left join restaurants on label = location group by label) as count_restaurants
	join
	(select label as l2, count(concat(id, '-', tag)) as num_drones from locations left join drones on label = hover group by label) as count_drones
	on l1 = l2
) as temp
on l1 = count_services.label);

-- [28] display_ingredient_view()
-- -----------------------------------------------------------------------------
/* This view displays information in the system from the perspective of the ingredients.
For each ingredient that is being carried by at least one drone, it includes a list of
the various locations where it can be purchased, along with the total number of packages
that can be purchased and the lowest and highest prices at which the ingredient is being
sold at that location. */
-- -----------------------------------------------------------------------------
create or replace view display_ingredient_view as
select I.iname as ingredient_name, hover as location, quantity as amount_available, price as low_price, price as high_price 
from( 
(ingredients as I) 
inner join 
(payload as PL left join drones as D on PL.tag = D.tag and PL.id = D.id) 
on I.barcode = PL.barcode);

-- [29] display_service_view()
-- -----------------------------------------------------------------------------
/* This view displays information in the system from the perspective of a delivery
service.  It includes the identifier, name, home base location and manager for the
service, along with the total sales from the drones.  It must also include the number
of unique ingredients along with the total cost and weight of those ingredients being
carried by the drones. */
-- -----------------------------------------------------------------------------
create or replace view display_service_view as
select  service_d.id, long_name, home_base, manager, ifnull(revenue,0) as revenue, ifnull(ingredients_carried,0) as ingredients_carried, 
ifnull(cost_carried,0) as cost_carried, ifnull(weight_carried,0) as weight_carried from(
	(select service.id, long_name, home_base, manager, revenue from(
	(select id, long_name, home_base, manager from delivery_services) as service
	left outer join
	(select id, sum(sales) as revenue from drones group by id) as reve
	on service.id = reve.id)) as service_d
    left outer join
    (select p.id, count(distinct p.barcode) as ingredients_carried, sum(quantity * price) as cost_carried,  sum(quantity *weight) as weight_carried from (
		(select * from payload) as p
		join 
		(select barcode, weight from ingredients) as i
		on p.barcode = i.barcode
		)group by id
    ) as service_carry
    on service_d.id = service_carry.id
);

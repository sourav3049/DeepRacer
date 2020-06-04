def reward_function(params):
    import math
    
    #Declaring constants
    MAX_REWARD = 1e2
    MIN_REWARD = 1e-3
    DIRECTION_THRESHOLD = 10.0
    ABS_STEERING_THRESHOLD = 15.0
    TOTAL_NUM_STEPS = 300.0
    SPEED_THRESHOLD = 4.0
    
    # Read input parameters
    on_track = params['all_wheels_on_track']
    distance_from_center = params['distance_from_center']
    track_width = params['track_width']
    steering = params['steering_angle'] # Only need the absolute steering angle for calculations
    speed = params['speed']
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints'] 
    heading = params['heading']
    off_track = params['is_offtrack']
    progress = params['progress']
    steps=params['steps']
    left_drive = params['is_left_of_center']
    track_length = params['track_length']
    # Declare default reward
    reward = 0.00001
    
    #reward function 
    
    #Ensure on car in on track
    
    
    #Calculate the direction of the center line based on the closest waypoints    
    def direction_reward(current_reward, waypoints, closest_waypoints, heading,left_drive,speed):

        next_point = waypoints[closest_waypoints[1]]
        prev_point = waypoints[closest_waypoints[0]]

        # Calculate the direction in radius, arctan2(dy, dx), the result is (-pi, pi) in radians
        direction = math.atan2(next_point[1] - prev_point[1], next_point[0] - prev_point[0]) 
        # Convert to degrees
        direction = math.degrees(direction)

        # Cacluate difference between track direction and car heading angle
        direction_diff = abs(direction - heading)

        if direction_diff > 180.0:
            direction_diff = 360.0 - direction_diff
        
        # Penalize if the difference is too large
        if direction_diff > DIRECTION_THRESHOLD:
            current_reward *= 0.5
        elif (steering <0 and left_drive == True) or (steering >0 and left_drive == False):
            current_reward *= 0.2
        else:
            current_reward += 1/(abs(steering)+direction_diff+0.01)
        
        # increase speed if its moving in a strating line 
        if (direction_diff < 5 ) and ( 2.8 < speed <= 4 ):
            current_reward += 100 * (speed**2)
        else:
            current_reward *= 0.6
        
        return current_reward

    def on_track_reward(current_reward, on_track):
        if not on_track:
            current_reward = MIN_REWARD
        else:
            current_reward += MAX_REWARD
        return current_reward
    
    def speed_reward(current_reward, speed):
     	current_reward += (speed**2 / 4) * 10
     	return current_reward
    
    def steering_reward(current_reward , steering, speed):
        if abs(steering) < ABS_STEERING_THRESHOLD and speed > 1:
            current_reward += (speed**2) * 10
        return current_reward 
        
    def progress_completion (current_reward, steps, progress):
        current_reward += progress
        if (steps % 100) == 0 and progress > (steps / TOTAL_NUM_STEPS) * 100 :
            current_reward += 10.0
        if progress == 100:
        	current_reward += 5000
        return current_reward
    
    
    #Estimate Rewards
    reward = direction_reward(reward, waypoints, closest_waypoints, heading,left_drive,speed)
    reward = speed_reward(reward, speed)
    reward = steering_reward (reward, steering , speed)
    reward = progress_completion(reward, steps, progress)
    reward = on_track_reward(reward, on_track)
    #reward = time_reward(reward , speed , progress , track_length)
    
    return float(reward)

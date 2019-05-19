User
  - django default

Profile
  - username
  - email
  - avatar
  - bio
  - sex
  - addr
    + street, apt
    + city
    + state
    + country
    + zip
  - fav_cuisine

Review
  - author
  - datetime
  - comment
  - rating
  - user_fk
  - image (optional)
  - tipping

GuestPost (for guest)
  - guest_id
  - content      (intro, what i need)
  - cuisine_type (chinese, korean, italian)
  - create_datetime
  - event_datetime
  - status       (if a host has accepted the request)
  - host_id
  - event_id     (hostpost_id)

HostPost (for host)
  - host_id
  - content    (what guest needs to bring)
  - sample_img (optional)
  - cuisine_ype
  - create_datetime
  - event_datetime
  - addr
    + street, apt
    + city
    + state
    + country
    + zip
  - status     (if len(guest_list) == num_guests)
  - num_guests
  - guest_list

Transaction/MealHistory
  - host_id
  - guests_list
  - event_id

ChatMessage
  - 
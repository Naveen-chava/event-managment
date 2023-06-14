# Event Managment System
Event Management System - Appkonx Take Home Assignment

There two types of User Profile:
1. User
2. Admin

There are three user related models.
1. User model which is a base for both the profiles.
2. UserProfile  
3. StaffProfile (there's an is_admin field which can be used to make a staff profile as admin user)

A User can have both the UserProfile and StaffProfile

REST APIs:
1. Create User
2. Create UserProfile
3. Create StaffProfile
4. Login User

Admin APIs:
1. Create Event
2. Update Event
3. Get Event
4. Get All Events

User APIs:
1. Get an Event
2. Get All Events
3. Ticket Booking
4. Get All Tickets
5. Get All Tickets booked for an event

Note: More APIs to be added soon


## Coverage Report
```

Name                                                                 Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------------
account/admin.py                                                         4      0   100%
account/api/serializers.py                                              19      0   100%
account/api/urls.py                                                      4      0   100%
account/api/views.py                                                    45      0   100%
account/apps.py                                                          4      0   100%
account/migrations/0001_initial.py                                      10      0   100%
account/models.py                                                       55      5    91%   25, 79, 83, 92, 108
account/tests.py                                                       125      0   100%
common/abstract_models.py                                               25      0   100%
common/abstract_test_setups.py                                          23      0   100%
common/constants.py                                                     41      1    98%   23
common/decorators.py                                                    14      0   100%
common/permissions.py                                                    9      4    56%   12-15
event/admin.py                                                           4      0   100%
event/api/serializers.py                                               110     24    78%   119-120, 123-124, 127, 130, 133-138, 141, 144, 171, 174, 177, 180, 183, 186-187, 190-191, 194, 197
event/api/urls.py                                                        4      0   100%
event/api/views.py                                                      77     36    53%   42-45, 54-59, 62-67, 74-77, 84-89, 96-99, 102-105, 112-115
event/apps.py                                                            4      0   100%
event/migrations/0001_initial.py                                         9      0   100%
event/migrations/0002_remove_bookingwindow_external_id_and_more.py       6      0   100%
event/models.py                                                        127     56    56%   15, 18-21, 24-27, 30-33, 36-39, 55, 58, 61-64, 67, 70-73, 76-79, 85-89, 92-95, 98-102, 105, 117, 121, 139, 151, 155-158, 166, 174
event/tests.py                                                          78      0   100%
event_management/asgi.py                                                 4      4     0%   10-16
event_management/settings.py                                            29      0   100%
event_management/urls.py                                                 3      0   100%
event_management/wsgi.py                                                 4      4     0%   10-16
manage.py                                                               12      2    83%   12-13
services/account.py                                                     80      3    96%   23-24, 37
services/event.py                                                      189     91    52%   22, 25, 28, 31, 34, 37, 41, 44, 47, 50, 64, 107, 109, 159, 163-167, 171-175, 179-183, 187-191, 197-253, 259-279, 285-289, 293-297
--------------------------------------------------------------------------------------------------
TOTAL                                                                 1118    230    79%

```

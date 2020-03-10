### Database specification, Group Project Manager, CSCI3100
* user
  * user_id
  * username
  * email
  * (any personal information if needed)
* login
  * user_id
  * login_password
* project
  * project_id
  * project_name
* project_member
  * project_id
  * user_id
* chatroom
  * chatroom_id
  * project_id
  * record_id 
* chatroom_record
  * record_id
  * record_content
* share_file
  * file_id
  * file_type
  * file_size
  * project_id

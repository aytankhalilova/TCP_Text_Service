# TCP_Text_Service
    This is client-server-based console app “text_service”.
    
 # Scenario 
 * change_text: The sender sends the text file to the server and the json file, in respond the server must read the json file and swap the words from the text according the json file.
 * encode_decode text: The sender sends the text file and the key (another text) on the respond the server must XOR the text message with the key (One Time Pad cipher) and return it to the client. The decoding process happens in the same way where instead of the text message the client sends.
 
 # Installation
 To download console app, you need to type following command:
  * git clone https://github.com/aytankhalilova/TCP_Text_Service.git
  
 Then install requirements to have all packets needed for this project:
 * pip install requirements.txt
 
 # Usage
 For server and client, open 2 terminal tabs and run the following commands:
 * Server <br />
  python TCP_Server.py <br />
 
 * Client <br />
  python TCP_Client.py --mode change_text sample_source_file.txt sample_json_file.json <br />
 OR <br />
  python TCP_Client.py --mode encode_decode sample_source_file.txt sample_key.txt
 
 

import asyncio, pygame, io, logging, os, logger
import warnings
from contextlib import asynccontextmanager
from PyCharacterAI import Client
from asyncio import WindowsSelectorEventLoopPolicy
from PyCharacterAI.exceptions import AuthenticationError, SessionClosedError 
from config import CHAR_ID
from dotenv import load_dotenv

# Filter out the specific warning
warnings.filterwarnings('ignore', message='Curlm alread closed!')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize pygame mixer at startup
pygame.mixer.init()

load_dotenv()

# Get token from environment variable
char_token = os.getenv('CHARACTER_AI_TOKEN')
if not char_token:
    logger.error("CHARACTER_AI_TOKEN environment variable is not set")
    raise ValueError("Please set the CHARACTER_AI_TOKEN environment variable")

asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())

@asynccontextmanager
async def get_client():
    client = Client()
    try:
        await client.authenticate(char_token)
        yield client
    finally:
        if hasattr(client, '_session') and not client._session.closed:
            await client._session.close()

async def tulga_bot(char_name, prompt, mode="text"):
    async with get_client() as client:
        try:
            data = CHAR_ID[char_name]
            char_id = data['char_id']
            voice_id = data['voice_id']
            
            # Create chat session
            try:
                chat, greeting_turn = await client.chat.create_chat(char_id)
                greeting_message = greeting_turn.get_primary_candidate().text
                print(f"[{char_name}]: {greeting_message}")  
            except Exception as e:
                logger.error(f"Failed to create chat: {e}")
                return
            
            # Initial message
            try:
                response = await client.chat.send_message(char_id, chat.chat_id, prompt)
                if response and response.get_primary_candidate():
                    char_response = response.get_primary_candidate().text
                else:
                    logger.error("No response received from character")
                    return
            except Exception as e:
                logger.error(f"Failed to send initial message: {e}")
                return
            
            while True:  # Continuous conversation loop
                print(f'[{char_name}]: {char_response}')
                if mode == "voice":
                    try:
                        primary_candidate = response.get_primary_candidate()
                        if not primary_candidate:
                            logger.error(f"No primary candidate found for message")
                            continue
                        
                        candidate_id = primary_candidate.candidate_id
                        speech_bytes = await client.utils.generate_speech(
                            chat_id=chat.chat_id,
                            turn_id=response.turn_id,
                            candidate_id=candidate_id,
                            voice_id=voice_id
                        )
                        
                        if pygame.mixer.get_init():
                            sound = pygame.mixer.Sound(io.BytesIO(speech_bytes))
                            sound.play()
                            while pygame.mixer.get_busy():
                                await asyncio.sleep(0.1)
                            sound = None
                        else:
                            logger.error("pygame mixer not initialized")
                    except Exception as e:
                        logger.error(f"Error during voice playback: {e}")
                
                # Get next user input
                try:
                    user_input = input("[You]: ")
                    if user_input.lower() in ['quit', 'exit', 'bye']:
                        print("Ending conversation...")
                        break
                    
                    response = await client.chat.send_message(char_id, chat.chat_id, user_input)
                    if not response:
                        logger.error("No response received")
                        continue
                        
                    char_response = response.get_primary_candidate().text
                except KeyboardInterrupt:
                    print("\nConversation interrupted by user.")
                    break
                except Exception as e:
                    logger.error(f"Error getting response: {e}")
                    break

        except AuthenticationError:
            logger.error("Authentication error occurred")
        except SessionClosedError:
            logger.error("Session closed error occurred")
        except Exception as e:
            logger.error(f"An error occurred: {e}")

async def main():
    try:
        while True:
            mode = input("Enter mode (voice/text): ").lower()
            if mode not in ['voice', 'text']:
                print("Invalid mode. Please enter 'voice' or 'text'")
                continue
            break
        
        char_list = list(CHAR_ID.keys())
        print("\nAvailable characters:")
        for i, char in enumerate(char_list, 1):
            print(f"{i}. {char}")
        
        while True:
            try:
                char_choice = int(input("\nChoose character number: "))
                if 1 <= char_choice <= len(char_list):
                    char_name = char_list[char_choice - 1]
                    break
                print("Invalid choice. Please select a valid number.")
            except ValueError:
                print("Please enter a valid number.")
        
        prompt = input("[You]: ")
        # print(f"\nStarting conversation with {char_name} in {mode} mode...\n")
        await tulga_bot(char_name=char_name, prompt=prompt, mode=mode)
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
    finally:
        if pygame.mixer.get_init():
            pygame.mixer.quit()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nProgram terminated by user")
    finally:
        if pygame.mixer.get_init():
            pygame.mixer.quit() 
import pygame
import sys

#EXACTLY ONE OCCURRENCE OF "BBA"
pygame.init()
WIDTH, HEIGHT = 1200, 600  
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Exactly One Occurence of BBA Visualization")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

#Para ubos jud siya sa transition table hehe
circle_positions = {
    'q0': (100, 500),
    'q1': (250, 500),
    'q2': (400, 500),
    'q3': (550, 500),
    'q4': (700, 500),
    'q5': (850, 500),
    'q6': (1000, 500),
}

# Transition table for DFA
transitions = {
    ('q0', 'b'): 'q1', ('q0', 'a'): 'q0',
    ('q1', 'b'): 'q2', ('q1', 'a'): 'q0',
    ('q2', 'b'): 'q2', ('q2', 'a'): 'q3',
    ('q3', 'a'): 'q4', ('q3', 'b'): 'q4',
    ('q4', 'a'): 'q5', ('q4', 'b'): 'q5',
    ('q5', 'a'): 'q6', ('q5', 'b'): 'q5',
    ('q6', 'a'): 'q6', ('q6', 'b'): 'q6',
}

final_states = ['q3', 'q4', 'q5']
dead_state = 'q6'

font = pygame.font.SysFont(None, 36)

def draw_line(start_pos, end_pos, color=BLACK):
    pygame.draw.line(screen, color, start_pos, end_pos, 2)  #line para circles 


def draw_transition_table():
    header = font.render("Transition Table", True, BLACK)
    screen.blit(header, (50, 110))

    table_start_x = 350
    table_start_y = 110
    cell_width = 120
    cell_height = 40
    pygame.draw.rect(screen, BLACK, (table_start_x, table_start_y, cell_width * 3, cell_height * 8), 2)

    #headers
    screen.blit(font.render("STATE", True, BLACK), (table_start_x + 10, table_start_y + 5))
    screen.blit(font.render("0 (a)", True, BLACK), (table_start_x + cell_width + 10, table_start_y + 5))
    screen.blit(font.render("1 (b)", True, BLACK), (table_start_x + cell_width * 2 + 10, table_start_y + 5))

    # The Transition Table mam
    transitions_list = [
        ("0", "0", "1"),
        ("1", "0", "2"),
        ("2", "3", "2"),
        ("3", "3", "4"),
        ("4", "3", "5"),
        ("5", "6", "5"),
        ("6", "6", "6"),
    ]

    for i, (state, a, b) in enumerate(transitions_list):
        y = table_start_y + cell_height * (i + 1)
        screen.blit(font.render(state, True, BLACK), (table_start_x + 10, y + 5))
        screen.blit(font.render(a, True, BLACK), (table_start_x + cell_width + 10, y + 5))
        screen.blit(font.render(b, True, BLACK), (table_start_x + cell_width * 2 + 10, y + 5))
        pygame.draw.line(screen, BLACK, (table_start_x + cell_width, y), (table_start_x + cell_width, y + cell_height))  # Vertical lines
        pygame.draw.line(screen, BLACK, (table_start_x + cell_width * 2, y), (table_start_x + cell_width * 2, y + cell_height))

    #line to separate header
    pygame.draw.line(screen, BLACK, (table_start_x, table_start_y + cell_height), (table_start_x + cell_width * 3, table_start_y + cell_height))

# DFA with transitions para ni visualization of the states
def draw_dfa(current_state):

    # Draw transition lines between states
    for (from_state, symbol), to_state in transitions.items():
        start_pos = circle_positions[from_state]
        end_pos = circle_positions[to_state]
        draw_line(start_pos, end_pos)

    # Draw circles for each state
    for state, pos in circle_positions.items():
        color = GREEN if state in final_states else RED if state == dead_state else BLUE #hehe
        pygame.draw.circle(screen, color, pos, 40)
        pygame.draw.circle(screen, BLACK, pos, 40, 2)  # Circle border
        text = font.render(state, True, BLACK)
        screen.blit(text, (pos[0] - 20, pos[1] - 20))

    #mu highlight sa circle
    pygame.draw.circle(screen, (255, 255, 0), circle_positions[current_state], 40, 5) 

# kapoy naman ang self loop ibutang ... medyo kuti najud ning highlight diri lang ko taman hahah
def validate_string(input_string):
    state = 'q0'
    result = ""
    state_sequence = []  #visited nodes
    for symbol in input_string:
        previous_state = state 
        state_sequence.append(state)  #add sa seq
        state = transitions.get((state, symbol), 'q6')
        draw_dfa(state)  # Highlight the current state
        pygame.display.update()
        pygame.time.delay(1000) 
    state_sequence.append(state)
    if state in final_states:
        result = "Accepted"
    else:
        result = "Rejected"
    
    return result, state_sequence

def main():
    input_string = ""
    running = True
    result_text = ""
    state_sequence = ""
    while running:
        screen.fill(WHITE)
        draw_dfa('q0')   #initial state ang q0
        draw_transition_table()

        akong_name = font.render(f"Paul Thomas M. Abellana", True, BLACK)
        screen.blit(akong_name, (50, 20))

        input_text = font.render(f"Input: {input_string}", True, BLACK)
        screen.blit(input_text, (50, 40))  

        state_display = font.render(f"State Sequence: {state_sequence}", True, BLACK)
        screen.blit(state_display, (50, 80))  

        result_display = font.render(f"Result of String: {result_text}", True, BLACK)
        screen.blit(result_display, (700, 40))  
        
        pygame.display.flip() 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    input_string = input_string[:-1]
                elif event.key == pygame.K_RETURN:
                    result_text, state_sequence = validate_string(input_string)  # Validate and get result
                    input_string = ""
                else:
                    input_string += event.unicode

    pygame.quit()

if __name__ == "__main__":
    main()

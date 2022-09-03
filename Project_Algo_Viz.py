import math
import pygame
import random

pygame.init()

class Viz_information:
    WHITE = 255, 255, 255
    BLACK = 0, 0, 0
    GREEN = 0, 255, 0
    RED = 255, 0, 0
    GREY = 128, 128, 128

    GRADIENT = [

        (128, 128, 128),
        (160, 160, 160),
        (192, 192, 192)

    ]

    Background_Color = WHITE

    TOP_PAD = 150
    SIDE_PAD = 100

    FONT = pygame.font.SysFont('comicsans', 18)
    LARGE_FONT = pygame.font.SysFont('comicsans', 28)

    def __init__(self, width, height, lst):
        self.width = width
        self.height = height

        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Algorithms Visulization")
        self.set_lst(lst)
        

    def set_lst(self, lst):
        self.lst = lst
        self.min_val = min(lst)
        self.max_val = max(lst)
        
        self.block_width = round((self.width - self.SIDE_PAD) // len(lst))
        self.block_height = math.floor((self.height - self.TOP_PAD) / (self.max_val - self.min_val))
        self.start_x = self.SIDE_PAD // 2

def Viz(viz_info, algo_name, acending, sorting_algo):
    viz_info.window.fill(viz_info.Background_Color)
    
    controls = viz_info.FONT.render("R - RESET | SPACE - START SORTING | A - ASCENDING ORDER | D - DECENDING ORDER", 1, viz_info.BLACK)
    viz_info.window.blit(controls, (viz_info.width/2 - controls.get_width()/2, 5))

    sorting = viz_info.FONT.render("I - INSERTION SORT | B - BUBBLE SORT | S - SELECTION SORT", 1, viz_info.BLACK)
    viz_info.window.blit(sorting, (viz_info.width/2 - sorting.get_width()/2, 35))

    Title = viz_info.LARGE_FONT.render(f"{algo_name} - {'Ascending' if acending else 'Descending'}", 1, viz_info.RED)
    viz_info.window.blit(Title, (viz_info.width/2 - Title.get_width()/2, 75))

    Complexity = viz_info.FONT.render(f"{algo_name} - {'O(n^2)' if sorting_algo == Bubble_sort or sorting_algo == Insertion_sort or sorting_algo == Selection_sort else 'O(nlog(n))'}", 1, viz_info.BLACK)
    viz_info.window.blit(Complexity, (viz_info.width/2 - Complexity.get_width()/2, 125))
    
    draw_list(viz_info)  
    pygame.display.update()



def draw_list(viz_info, color_postion = {}, clear_background = False):
    lst = viz_info.lst
    
    if clear_background:
        clear_rectangle = (viz_info.SIDE_PAD//2, viz_info.TOP_PAD, viz_info.width - viz_info.SIDE_PAD, viz_info.height - viz_info.TOP_PAD)
        pygame.draw.rect(viz_info.window, viz_info.Background_Color, clear_rectangle)

    for i, val in enumerate(lst):
        x = viz_info.start_x + i * viz_info.block_width
        y = viz_info.height - (val - viz_info.min_val) * viz_info.block_height

        color = viz_info.GRADIENT[i % 3]

        if i in color_postion:
            color = color_postion[i]

        pygame.draw.rect(viz_info.window, color, (x, y, viz_info.block_width, viz_info.height))

    if clear_background:
        pygame.display.update()

def generate_starting_lst(len_lst, min_val, max_val):
    
    lst = []
    
    for _ in range(len_lst):
        val = random.randint(min_val, max_val)
        lst.append(val)

    return lst

def Bubble_sort(viz_info, ascending = True):
    lst = viz_info.lst

    for i in range(len(lst)-1):
        for j in range(len(lst) - 1 - i):
            num1 = lst[j]
            num2 = lst[j+1]

            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                lst[j], lst[j+1] = lst[j+1], lst[j]
                draw_list(viz_info, {j: viz_info.GREEN, j+1: viz_info.RED}, True)
                yield True
    
    return lst

def Insertion_sort(viz_info, ascending = True):
    lst = viz_info.lst

    for i in range(1, len(lst)):
        current =  lst[i]

        while True:
            ascending_sort = i > 0 and lst[i-1] > current and ascending
            decending_sort = i > 0 and lst[i-1] < current and not ascending
            
            if not ascending_sort and not decending_sort:
                break

            lst[i] = lst[i-1]
            i = i - 1
            lst[i] = current
            draw_list(viz_info, {i-1: viz_info.GREEN, i: viz_info.RED}, True)
            yield True

    return lst

def Selection_sort(viz_info, ascending = True):
    lst = viz_info.lst
    
    for i in range(len(lst)):
        min_index = i
 
        for j in range(i + 1, len(lst)):
            if (lst[j] < lst[min_index] and ascending) or (lst[j] > lst[min_index] and not ascending):
                min_index = j

        (lst[i], lst[min_index]) = (lst[min_index], lst[i])
        draw_list(viz_info, {i: viz_info.GREEN, min_index: viz_info.RED}, True)
        yield True

    return lst

def main():
    
    run = True
    clock = pygame.time.Clock() 

    len_lst = 50
    min_val = 0
    max_val = 100

    lst = generate_starting_lst(len_lst, min_val, max_val)  
    viz_info = Viz_information(800, 600, lst)
    sorting = False
    ascending = True

    sorting_algo = Bubble_sort
    sorting_algo_name = "Bubble Sort"
    sorting_algo_generator = None

    #Viz(viz_info)

    while run:
        
        clock.tick(10)

        if sorting:
            try:
                next(sorting_algo_generator)
            except StopIteration:
                sorting = False
        else:
            Viz(viz_info, sorting_algo_name, ascending, sorting_algo)        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type != pygame.KEYDOWN:
                continue
                
            if event.key == pygame.K_r:
                lst = generate_starting_lst(len_lst, min_val, max_val)
                viz_info.set_lst(lst)
            
            elif event.key == pygame.K_SPACE and sorting == False:
                sorting = True
                sorting_algo_generator = sorting_algo(viz_info, ascending)
            
            elif event.key == pygame.K_a and not sorting:
                ascending = True
            
            elif event.key == pygame.K_d and not sorting:
                ascending = False
            
            elif event.key == pygame.K_i and not sorting:
                sorting_algo = Insertion_sort
                sorting_algo_name = "Insertion Sort"
            
            elif event.key == pygame.K_b and not sorting:
                sorting_algo = Bubble_sort
                sorting_algo_name = "Bubble Sort"

            elif event.key == pygame.K_s and not sorting:
                sorting_algo = Selection_sort
                sorting_algo_name = "Selection Sort"
    
    pygame.quit()

main()
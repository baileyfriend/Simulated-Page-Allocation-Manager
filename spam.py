'''
Bailey Freund
SPAM
4/1/17
'''

"""
STRUCTURES TO IMPLEMENT: 
1. a structure that mimics a process control block (PCB) of a process. A real PCB holds tons of information about a process, such as: pid, pointer (or index) to page table, size of segments, etc.
2. a page table data structure for mapping logical to physical addresses
3. implement a frame table (to simulate the contents of simulated RAM)
4. maintain the free frame list
5. other relevant data structures
"""
import math as math
# Define constants
page_size = float(512) # bytes
physical_memory = 4096 #bytes

num_frames = int(physical_memory/page_size) # 8 pages

# hardware_frames = { # dict of frames (by addr) mapped to whether they are free or not
#     0: 1, 
#     512: 1, 
#     1024: 1,
#     1536: 1,
#     2048: 1,
#     2560: 1,
#     3072: 1,
#     3584: 1
#     } # 1 means free, 0 means used - init to all free

# hardware_frames = { # dict of frames (by addr) mapped to whether they are free or not
#     0: 1,
#     1: 1, 
#     2: 1,
#     3: 1,
#     4: 1,
#     5: 1,
#     6: 1,
#     7: 1
#     }



"""
The memory manager simulation will proceed approximately as described below:
Your program (simulating the OS loader) is presented with the size of code and data segments of an executable to be loaded to memory
Given the page size of 512 bytes, the loader determines the number of pages for code and data segments. Note: they are mapped separately, i.e. your simulation program shall use two page tables per process: one for mapping pages of the text/code segment, and another one for data segment
Like an OS, your simulation program creates these page table structures for each process required to map logical page numbers to physical frame numbers.
It then inspects the list of free frames and allocate the number of required frames in the simulated RAM, claim these frames on behalf of the process.
It then updates the page table and list of free frames accordingly.
Your simulation program shall then display the process page tables showing the mapping of pages to frames for that process.
Your simulation program must also display the page frame table (showing the memory map of physical memory and its contents)
When a program terminates, all physical frames allocated to the process are reclaimed by the (simulated) OS, its page table is disposed and other relevant data structures are updated
"""

class Process:
    def __init__(self, pid, textsize, datasize, physical_memory):
        self.pid = pid
        self.textsize = float(textsize)
        self.datasize = float(datasize)

        self.text_page_table = PageTable(pid, textsize, 'text', physical_memory)
        self.data_page_table = PageTable(pid, datasize, 'data', physical_memory)

        self.pcb = PCB(self.pid, self.text_page_table, self.data_page_table, self.textsize + self.datasize)



class Row:
    def __init__(self, frame, segment, pid, page_num):
        self.frame = frame
        self.segment = segment
        self.pid = pid
        self.page_num = page_num
        self.is_free = False



class PhysicalMemory:
    def __init__(self):
        print('Created physical memory')
        self.free_frames = [0, 1, 2, 3, 4, 5, 6, 7] # all frames start free
        self.rows = []

        for i in range(num_frames):
            self.rows.append(Row(i, 'none', -1, -1))
    


    def add_pages(self, page_table):
        current_page_num = 0
        frames = []

        for frame in self.free_frames:

            if current_page_num == page_table.num_pages:
                print('EVENT: Process %s segment %s is put into physical memory' % (page_table.pid, page_table.segment))
                physical_memory.print_physical_memory()
                result = frames
                self.remove_from_free(frames)
                return result

            self.rows[frame] = Row(frame, page_table.segment, page_table.pid, current_page_num)
            current_page_num = current_page_num + 1
            frames.append(frame)
    


    def remove_from_free(self, added_frames):
        for frame in added_frames:
            self.free_frames.remove(frame)
        if self.free_frames is None:
            self.free_frames = []
    


    def halt(self, pid):
        for row in self.rows:
            if row.pid == pid: # if row matches pid being halted 
                if row.frame not in self.free_frames:
                    self.free_frames.append(row.frame)
                self.rows[row.frame] = Row(row.frame, 'none', -1, -1) # then set the row back to initial value
                
        print('EVENT: process %s terminates' % pid)
        physical_memory.print_physical_memory()

        
    def print_physical_memory(self):
        print('PHYSICAL MEMORY')
        print('frame       segment     pid     page num')
        for row in self.rows:
            print('%s           %s          %s          %s' % (row.frame, row.segment, row.pid, row.page_num))






class PageTable:
    def __init__(self, pid, size, segment, physical_memory):
        self.pid = pid
        self.size = size
        self.segment = segment
        # self.frames
        self.num_pages = math.ceil(size/page_size)
        self.frames = []
        
    
    def num_free_frames(self, physical_memory):
        return len(physical_memory.free_frames)

    def add(self, physical_memory):
        
        if self.num_pages <= self.num_free_frames(physical_memory): # then add
            self.frames = physical_memory.add_pages(self)
            #print(self.frames)
            self.print_page_table()
        else:
            print('Not enough room for pid %s, not adding page table' % self.pid)



    def print_page_table(self):
        print('Page table for pid %s segment %s' %(self.pid, self.segment))
        print('page     frame')
        page = 0
        if self.frames is None:
            self.frames = []

        for frame in self.frames:
            print('%s       %s' % (page, frame))

class PCB: 
    def __init__(self, pid, text_page_table, data_page_table, segment_size):
        self.pid = pid
        self.text_page_table_index = text_page_table
        self.data_page_table_index = data_page_table
        self.segment_size = segment_size

# class Loader:
#     def __init__(self, hardware_frames):
#         print('Loader initialized')
#         self.frames = hardware_frames
#         self.free_frames = 

#     def check_for_free_frames(self):
#         for frame, is_free in self.frames.items():
#             if is_free == 1:
#                 return frame
#         return 'No free frames'
            
    


if __name__ == '__main__':
    physical_memory = PhysicalMemory()
    with open("run", "r") as f: # https://stackoverflow.com/questions/35226903/python-3-5-1-reading-from-a-file
        content = f.read()
        run_list = content.split('\n') 
    

    for run_process in run_list:
        print('------------------------------------------------------------')
        run_process_split = run_process.split(' ')
        if run_process_split[1] != '-1':
            p = Process(run_process_split[0], float(int(run_process_split[1])), float(int(run_process_split[2])), physical_memory)
            p.text_page_table.add(physical_memory)
            p.data_page_table.add(physical_memory)
        else: # halt the process
            pid = run_process_split[0]
            physical_memory.halt(pid)

        
    
'''
Bailey Freund
SPAM
4/1/17
'''
# import
import math as math
import sys

# Define constants
page_size = float(512) # bytes
physical_memory = 4096 # bytes

num_frames = int(physical_memory/page_size) # 8 pages

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



class PageTable: # every process has 2 page tables - 1 for code(aka text) and one for data
    def __init__(self, pid, size, segment, physical_memory):
        self.pid = pid
        self.size = size
        self.segment = segment
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
    


if __name__ == '__main__':
    filename = sys.argv[1]
    print('Using file %s' % filename)

    physical_memory = PhysicalMemory()
    with open(filename, "r") as f: # https://stackoverflow.com/questions/35226903/python-3-5-1-reading-from-a-file
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

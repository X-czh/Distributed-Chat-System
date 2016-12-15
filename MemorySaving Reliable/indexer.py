class Index:
    def __init__(self, name, start_line = 0):
        self.name = name
        self.msgs = [];
        self.index = {}
        self.start_line = start_line
        self.total_msgs = 0
        
    def get_msg_size(self):
        return self.total_msgs
        
    def get_msg(self, n):
        return self.msgs[n - self.start_line]
        
    def add_msg(self, m):
        self.msgs.append(m)
        self.total_msgs += 1
        
    def add_msg_and_index(self, m):
        self.add_msg(m)
        line_at = self.start_line + self.total_msgs - 1
        self.indexing(m, line_at)

    def indexing(self, m, l):
        # lower the letters so that "Who" and "who" can be considered to be the same word
        words = m.lower().split()

        # remove trailing punctuation marks
        # when encountering the heading of a poem (len(words) == 1), pass
        punctuations = ',.?!:;"\''
        for i, w in enumerate(words):
            # Return a copy of the string with the leading and trailing characters removed. 
            # The chars argument is a string specifying the set of characters to be removed.
            if len(words) == 1 and w[-1] == '.' and w[-2].isupper():
                pass
            else:
                w = w.strip(punctuations)
            
            # index both the column number (line number) and the row number (the position of the word in that line)
            try:
                self.index[w].append((l, i))
            except KeyError:
                self.index[w] = []
                self.index[w].append((l, i))

    def search_idx(self, term):
        msgs = []
        # used to store the list of words in term
        words = term.split()
        # used to record the length of the phrase term, if 1 -> single word
        length = len(words)
        # used to remove duplicates
        line_index = set()
            
        # search for single words, also deal with null term
        if length <= 1:
            try:
                for i in self.index[term]:
                    if i[0] not in line_index:
                        line_index.add(i[0])
                        msgs.append(i[0])
            except KeyError:
                pass

        # search for phrases
        else:
            try:
                for i in self.index[words[0]]:
                    found = True
                    # checking the words right following the first word
                    for j in range(1, length):
                        if (i[0], i[1] + j) not in self.index[words[j]]:
                            found = False
                            break
                    if found:
                        if i[0] not in line_index:
                            line_index.add(i[0])
                            msgs.append(i[0])
            except KeyError:
                pass

        return msgs

    def search(self, term):
        if (term in self.index.keys()):
            indices = [i[0] for i in self.index[term]]
            msgs = [self.msgs[i] for i in indices]
            ret_msg = ''
            for m in msgs:
                ret_msg = ret_msg + m + '\n'
            return ret_msg
            #return (string.join(msgs,'\n'))
        else:
            return ('')
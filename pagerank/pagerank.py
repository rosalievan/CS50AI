import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    output = {}
    for key in corpus:
        output[key] = 0
    corpus_size = len(corpus)
    
    if corpus[page] == None:
        for key in corpus:
            output[key] = 1/ corpus_size
    
    else:
        for key in corpus:
            output[key] =  (1-damping_factor) / corpus_size

        num_links = len(corpus[page])
        for key1 in corpus[page]:
            output[key1] += damping_factor / num_links

    return output

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    sample = random.choice(list(corpus.keys()))
    output = {}
    for key in corpus:
        output[key] = 0
    counter = 0

    while counter < n :
        counter +=1
        output[sample] += 1
        sample_probs = transition_model(corpus, sample, damping_factor)
        sample = random.choices(list(sample_probs.keys()), weights=list(sample_probs.values()), k=1)[0]
    
    total = sum(output.values())
    for key in output:
        output[key] = output[key] / total
            
    return output
        
    # generate dictionary with pages as keys and count up per occurence
    # initiate sample
    # while number < n count up
    # generate next sample

    # at the end, in the output dictionary, divide each value by n and return
    


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    corpus_size = len(corpus)
    output = {}
    new_output= {}
    
    for key in corpus:
        output[key] = 1/corpus_size
        new_output[key] = 1/corpus_size

    constant = (1-damping_factor) / corpus_size
    while True:
        for p in output:
            link_follow_prob = 0
            for i in output:
                if p in corpus[i]:
                    link_follow_prob += (output[i] / len(corpus[i]))
                elif not corpus[i]:
                    link_follow_prob += 1 / corpus_size

            pr_p = constant + link_follow_prob
            new_output[p] = pr_p

        total = sum(new_output.values())
        for key in new_output:
            new_output[key] = new_output[key] / total
        
        if get_difference(output, new_output)<0.001:
            break

        output = new_output.copy()

    return new_output
        
        
def get_difference(output, new_output):
    differencedict = {key: output[key]-new_output[key] for key in output if key in new_output}
    max_difference = 0
    for key in differencedict:
        if differencedict[key] > max_difference:
            max_difference = differencedict[key]
    return max_difference

if __name__ == "__main__":
    main()

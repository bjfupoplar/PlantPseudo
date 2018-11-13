/*
 * Author: Yupeng Wang <wyp1125@uga.edu> March 31, 2011
 * Program for classifying the duplicate genes of a genome into WGD, tandem, proximal and dispersed duplicates
 * using MCScanX as a compoment
*/

#include "dup_classifier.h"

static bool IS_PAIRWISE;
static bool BUILD_MCL;
static char prefix_fn[LABEL_LEN];

static void print_banner()
{
    ;
}

static void init_opt()
{
    // match bonus, final score=MATCH_SCORE-GAPS^GAP_PENALTY
    MATCH_SCORE = 50;
    // the number of genes required to call synteny, sometimes more
    MATCH_SIZE = 5;
    // gap extension penalty
    GAP_PENALTY = -1;
    // alignment significance
    E_VALUE = 1e-5;
    // maximum gaps allowed
    MAX_GAPS =25;
    N_PROXIMAL =10;
    OVERLAP_WINDOW=5;
    IS_PAIRWISE = false;
    IN_SYNTENY = 0;
}

static void print_help(const char *prg)
{
    progress("[Usage] %s prefix_fn [options]\n"
             " -k  MATCH_SCORE, final score=MATCH_SCORE+NUM_GAPS*GAP_PENALTY\n"
             "     (default: %d)\n"
             " -g  GAP_PENALTY, gap penalty (default: %d)\n"
             " -s  MATCH_SIZE, number of genes required to call a collinear block\n"
             "     (default: %d)\n"
             " -e  E_VALUE, alignment significance (default: %lg)\n"
             " -w  OVERLAP_WINDOW, maximum distance (# of genes) to collapse BLAST matches (default: %d)\n"
             " -m  MAX_GAPS, maximum gaps allowed (default: %d)\n"
             " -n  N_PROXIMAL, maximum distance (# of genes) to call proximal (default: %d)\n"
             " -h  print this help page\n",
             prg, MATCH_SCORE, GAP_PENALTY, MATCH_SIZE, E_VALUE, OVERLAP_WINDOW, MAX_GAPS, N_PROXIMAL);
    exit(1);
}

static void read_opt(int argc, char *argv[])
{
    int c;
    opterr = 0;

    if (argc < 2) print_help(argv[0]);

    while ((c = getopt(argc, argv, "k:g:s:e:w:n:m:ah")) != -1)
        switch (c)
        {
        case 'k':
            MATCH_SCORE = atoi(optarg);
            break;
        case 'g':
            GAP_PENALTY = atoi(optarg);
            break;
        case 's':
            MATCH_SIZE = atoi(optarg);
            break;
        case 'e':
            E_VALUE = atof(optarg);
            break;
        case 'w':
            OVERLAP_WINDOW = atoi(optarg);
            break;
        case 'n':
            N_PROXIMAL = atoi(optarg);
            break;
        case 'm':
            MAX_GAPS = atoi(optarg);
            break;
        case '?':
            if (optopt=='k' || optopt=='s' || optopt=='g' || optopt=='e' || optopt=='w' || optopt=='m' || optopt=='n')
                errAbort("Option -%c requires an argument.", optopt);
            else if (isprint (optopt))
                errAbort("Unknown option `-%c'.", optopt);
            else
                errAbort("Unknown option character `\\x%x'.", optopt);
        default:
            print_help(argv[0]);
            break;
        }

    if (optind==argc) errAbort("Please enter your input file");
    else strcpy(prefix_fn, argv[optind]);
    CUTOFF_SCORE = MATCH_SCORE*MATCH_SIZE;
}
void fill_allg()
{
    Gene_feat *gf1;
    map<string, Gene_feat>::iterator it;
    for (it=gene_map.begin(); it!=gene_map.end(); it++)
    {
        gf1 = &(it->second);
        allg.insert(gf1);
    }
    int i=0;
    geneSet::const_iterator it77=allg.begin();
    for (; it77!=allg.end(); it77++)
    {
    (*it77)->gene_id=i;
    i++;
    }
}

int main(int argc, char *argv[])
{
    /* Start the timer */
    uglyTime(NULL);

    print_banner();
    char align_fn[LABEL_LEN], block_fn[LABEL_LEN],html_fn[LABEL_LEN];
    FILE *fw;

    init_opt();
    read_opt(argc, argv);

    read_gff(prefix_fn);
    read_blast(prefix_fn);

    progress("%d pairwise comparisons", (int) mol_pairs.size());
    fill_allg();
    map<string, int>::const_iterator ip;
    for (ip=mol_pairs.begin(); ip!=mol_pairs.end(); ip++)
    {
        if (ip->second >= MATCH_SIZE) feed_dag(string(ip->first));
    }

    progress("%d alignments generated", (int) seg_list.size());
    cls_main(prefix_fn);
    return 0;
}


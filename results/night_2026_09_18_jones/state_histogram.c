/* Exact Kauffman-state histogram, at most 20 crossings.
 * Input: n followed by n cyclic PD quadruples with labels 0,...,2n-1.
 * Bit 0: A-smoothing (0,1)(2,3); bit 1: B-smoothing (0,3)(1,2).
 * Arc labels are DSU vertices; connected components after smoothing are circles.
 * Output: b circles number_of_states. All counts fit in uint64_t since n<=20.
 */
#include <stdint.h>
#include <stdio.h>
#include <inttypes.h>

static int parent[40];
static int root(int x) {
    while (parent[x] != x) { parent[x] = parent[parent[x]]; x = parent[x]; }
    return x;
}
static void join(int a, int b) { a=root(a); b=root(b); if(a!=b) parent[a]=b; }
int main(void) {
    int n, pd[20][4], occurs[40]={0};
    uint64_t hist[21][41]={{0}};
    if(scanf("%d",&n)!=1 || n<1 || n>20) return 2;
    for(int i=0;i<n;i++) for(int j=0;j<4;j++) {
        if(scanf("%d",&pd[i][j])!=1 || pd[i][j]<0 || pd[i][j]>=2*n) return 3;
        occurs[pd[i][j]]++;
    }
    for(int i=0;i<2*n;i++) if(occurs[i]!=2) return 4;
    for(uint32_t state=0; state<(UINT32_C(1)<<n); state++) {
        int b=0, circles=0;
        for(int j=0;j<2*n;j++) parent[j]=j;
        for(int i=0;i<n;i++) {
            int *q=pd[i];
            if((state>>i)&1) { b++; join(q[0],q[3]); join(q[1],q[2]); }
            else { join(q[0],q[1]); join(q[2],q[3]); }
        }
        for(int j=0;j<2*n;j++) if(root(j)==j) circles++;
        hist[b][circles]++;
    }
    for(int b=0;b<=n;b++) for(int l=1;l<=2*n;l++)
        if(hist[b][l]) printf("%d %d %" PRIu64 "\n",b,l,hist[b][l]);
    return 0;
}

// Exact Kauffman-bracket frontier contraction of a planar diagram.
// Each closed smoothing circle evaluates to delta=-x-x^{-1}, x=A^2.
// Factoring A^{-1} from each crossing leaves weights x and 1.
// The coefficient ring is Z[x]/((x^2+1)^5), or its mod-32 reduction.
#include <array>
#include <vector>
#include <string>
#include <unordered_map>
#include <map>
#include <set>
#include <algorithm>
#include <iostream>
#include <chrono>
#include <stdexcept>
#ifdef EXACT
#include <boost/multiprecision/cpp_int.hpp>
using Int=boost::multiprecision::cpp_int;
#else
using Int=int;
#endif
constexpr int N=10;
using Poly=std::array<Int,N>;
inline void normalize(Poly &a){
#ifndef EXACT
 for(auto &v:a){v%=32;if(v<0)v+=32;}
#endif
}
Poly mulx(const Poly&a){
 Poly r{};for(int i=1;i<N;i++)r[i]=a[i-1];
 static const int binom[]={1,5,10,10,5};
 for(int j=0;j<5;j++)r[2*j]-=binom[j]*a[N-1];normalize(r);return r;
}
Poly divx(const Poly&a){
 Poly r{};for(int i=0;i<N-1;i++)r[i]=a[i+1];
 static const int binom[]={5,10,10,5,1};
 for(int j=0;j<5;j++)r[2*j+1]-=binom[j]*a[0];normalize(r);return r;
}
Poly delta(const Poly&a){
 auto r=mulx(a),s=divx(a);for(int i=0;i<N;i++)r[i]=-r[i]-s[i];normalize(r);return r;
}
bool zero(const Poly&a){for(const auto&v:a)if(v!=0)return false;return true;}
void accum(Poly&a,const Poly&b){for(int i=0;i<N;i++)a[i]+=b[i];normalize(a);}
struct DSU{
 int a[96],nc;
 explicit DSU(int n):nc(n){for(int i=0;i<n;i++)a[i]=i;}
 int root(int x){while(a[x]!=x){a[x]=a[a[x]];x=a[x];}return x;}
 void join(int x,int y){x=root(x);y=root(y);if(x!=y){a[x]=y;--nc;}}
};
int main(){try{
 int crossings,writhe,extra_loops;
 if(!(std::cin>>crossings>>writhe>>extra_loops))return 2;
 std::vector<std::array<int,4>> pd(crossings);for(auto& c:pd)for(auto&e:c)std::cin>>e;
 std::vector<int> order(crossings);for(auto&i:order)std::cin>>i;
 {auto s=order;std::sort(s.begin(),s.end());for(int i=0;i<crossings;i++)if(s[i]!=i)throw std::runtime_error("bad order");}
 std::map<int,int> count;for(auto c:pd)for(int e:c)count[e]++;for(auto x:count)if(x.second!=2)throw std::runtime_error("bad PD multiplicity");
 std::unordered_map<std::string,Poly> states;Poly one{};one[0]=1;states[""]=one;
 std::vector<int> boundary;size_t maxstates=1;int maxwidth=0;
 auto start=std::chrono::steady_clock::now();
 for(int step=0;step<crossings;step++){
  const auto &cross=pd[order[step]];
  std::vector<int> nodes=boundary;for(int e:cross)if(std::find(nodes.begin(),nodes.end(),e)==nodes.end())nodes.push_back(e);
  if(nodes.size()>96)throw std::runtime_error("frontier too wide");
  std::set<int> newset(boundary.begin(),boundary.end());for(int e:cross){if(newset.count(e))newset.erase(e);else newset.insert(e);}
  std::vector<int> nextboundary(newset.begin(),newset.end());std::vector<int> exterior;
  for(int e:nextboundary)exterior.push_back(std::find(nodes.begin(),nodes.end(),e)-nodes.begin());
  int port[4];for(int j=0;j<4;j++)port[j]=std::find(nodes.begin(),nodes.end(),cross[j])-nodes.begin();
  std::unordered_map<std::string,Poly> result;result.reserve(states.size()*2+1);
  for(const auto &kv:states){
   const auto &key=kv.first;const auto &coeff=kv.second;
   if(zero(coeff))continue;
   for(int s=0;s<2;s++){
    DSU d(nodes.size());
    for(int i=0;i<(int)boundary.size();i++)if(i<(unsigned char)key[i])d.join(i,(unsigned char)key[i]);
    if(s==0){d.join(port[0],port[1]);d.join(port[2],port[3]);}
    else{d.join(port[0],port[3]);d.join(port[1],port[2]);}
    int first[96];std::fill(first,first+96,-1);std::string newkey(exterior.size(),char(255));
    for(int k=0;k<(int)exterior.size();k++){
     int root=d.root(exterior[k]);if(first[root]==-1)first[root]=k;
     else {int j=first[root];if((unsigned char)newkey[j]!=255)throw std::runtime_error("not a pairing");newkey[j]=char(k);newkey[k]=char(j);}
    }
    for(unsigned char x:newkey)if(x==255)throw std::runtime_error("open unmatched endpoint");
    int loops=d.nc-(int)exterior.size()/2;if(loops<0||loops>2)throw std::runtime_error("unexpected loop count");
    auto val=(s==0?mulx(coeff):coeff);for(int k=0;k<loops;k++)val=delta(val);
    if(!zero(val))accum(result[newkey],val);
   }
  }
  for(auto it=result.begin();it!=result.end();){if(zero(it->second))it=result.erase(it);else++it;}
  states.swap(result);boundary.swap(nextboundary);maxstates=std::max(maxstates,states.size());maxwidth=std::max(maxwidth,(int)boundary.size());
  if(step%16==15||step==crossings-1){double elapsed=std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();std::cerr<<"step="<<step+1<<" boundary="<<boundary.size()<<" states="<<states.size()<<" seconds="<<elapsed<<std::endl;}
  if(states.size()>2000000)throw std::runtime_error("STATE_CAP_UNKNOWN");
 }
 if(!boundary.empty())throw std::runtime_error("nonempty final frontier");
 auto val=states[""];for(int i=0;i<extra_loops;i++)val=delta(val);
 if((crossings+3*writhe)%2)throw std::runtime_error("nonintegral normalization");
 int exponent=(-crossings-3*writhe)/2;
 for(int i=0;i<abs(exponent);i++)val=(exponent<0?divx(val):mulx(val));
 if(writhe%2)for(auto&v:val)v=-v;normalize(val);
 double elapsed=std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();
 std::cout<<"{\"coefficients_x\":[";for(int j=0;j<N;j++){if(j)std::cout<<",";std::cout<<val[j];}
 std::cout<<"],\"order\":5,\"modulus\":";
#ifdef EXACT
 std::cout<<"null";
#else
 std::cout<<"32";
#endif
 std::cout<<",\"crossings\":"<<crossings<<",\"writhe\":"<<writhe<<",\"max_states\":"<<maxstates<<",\"max_frontier\":"<<maxwidth<<",\"seconds\":"<<elapsed<<"}"<<std::endl;
 return 0;
 }catch(const std::exception&e){std::cerr<<e.what()<<std::endl;return 3;}}

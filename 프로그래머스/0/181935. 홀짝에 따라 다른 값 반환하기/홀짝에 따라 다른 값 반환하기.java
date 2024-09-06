class Solution {
    public int solution(int n) {
        int answer = 0;
        if(n%2==0){
            for(int i=0;i<=n;i+=2){
                answer += i*i;
            }
        } else{
            for(int i=0;i<=n;i+=2){
                answer += i+1;
            }
        }
            
        return answer;
    }
}
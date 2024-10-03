class Solution {
    public int solution(int num) {
        long answer = num;
        int n=0;
        while(n<500){
        if(answer==1) {return n;}
            
            if (answer % 2 == 0) {
                answer = answer / 2; 
            } else {
                answer = answer * 3 + 1;
            }
        
            n++;
        }
        return -1;
}
}
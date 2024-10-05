import java.util.Arrays;

class Solution {
    public int solution(int[] d, int budget) {
        int answer = 0;
        int index  = 0;
        Arrays.sort(d);
        while(index<d.length&&answer+d[index]<=budget){
            answer += d[index];
            index++;
        }
        return index;
    }
}
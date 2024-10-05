import java.util.*;

public class Solution {
    public int[] solution(int []arr) {

        HashSet<Integer> set = new HashSet<>();
        for(int a : arr){
            set.add(a);
        }
        int[] answer = new int[set.size()];
        int index = 0;
        for(int a : set){
            answer[index++] = a;
        }
        
        return answer;
    }
}
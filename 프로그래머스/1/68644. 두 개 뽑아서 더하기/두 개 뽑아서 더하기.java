import java.util.HashSet;
import java.util.ArrayList;
import java.util.Collections;

class Solution {
    public int[] solution(int[] numbers) {
        HashSet<Integer> set = new HashSet<>();
        for(int i=0;i<numbers.length;i++){
            for(int j=i+1;j<numbers.length;j++){
                set.add(numbers[i]+numbers[j]);
                }
        }
        ArrayList<Integer> list = new ArrayList(set);
        Collections.sort(list);
        int[] answer = new int[list.size()];
        for(int i=0;i<list.size();i++){
            answer[i] = list.get(i);
        }
        
        return answer;
    }
}
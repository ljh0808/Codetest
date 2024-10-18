import java.util.*;

class Solution {
    public int[] solution(int[] array, int[][] commands) {
        int[] answer = new int[commands.length];
        
        for(int i=0;i<commands.length;i++){
         ArrayList<Integer> list = new ArrayList<>();
            int j = commands[i][0]-1;
            int k = commands[i][1]-1;
            for(;j<=k;j++){
                list.add(array[j]);
            }
            Collections.sort(list);
            answer[i] = list.get(commands[i][2]-1);
        }
        
        return answer;
    }
}
class Solution {
    public boolean solution(int x) {
        boolean answer = false;
        String str = x+"";
        int sum=0;
        String[] result = str.split("");
        for(int i=0;i<result.length;i++){
            sum += Integer.parseInt(result[i]);
        }
        if(x%sum==0) answer=true;
        return answer;
    }
}
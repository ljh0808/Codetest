class Solution {
    public String solution(int[] food) {
        String answer = "";
        StringBuilder sb  = new StringBuilder();
        StringBuilder sb2 = new StringBuilder();
        for(int i=1;i<food.length;i++){
            int num = food[i]/2;
            for(;num>0;num--){
                sb.append(i);
            }
        }
        sb2.append(sb);
        sb2.append("0");
        sb2.append(sb.reverse());
        return sb2.toString();
    }
}
class Solution {
    public int solution(int[][] sizes) {
        int w = 0;
        int h = 0;
        
        for(int i=0;i<sizes.length;i++){
            if(sizes[i][0]<sizes[i][1]){
                int num     = sizes[i][0];
                sizes[i][0] = sizes[i][1];
                sizes[i][1] = num;
            }
            if(w<sizes[i][0])  w=sizes[i][0];
            if(h<sizes[i][1])  h=sizes[i][1];
        }
        return h*w;
    }
}
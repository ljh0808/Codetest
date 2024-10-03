class Solution {
    public String solution(String[] seoul) {
       String answer = "김서방은 ";
		        int num=0;
		        for(int i=0;i<seoul.length;i++){
		        	System.out.println(seoul[i]);
		            if(seoul[i].equals("Kim")) num=i;
		        }
		 StringBuilder sb = new StringBuilder();
		 sb.append(answer + num+"에 있다");
		 return sb.toString();
}
}
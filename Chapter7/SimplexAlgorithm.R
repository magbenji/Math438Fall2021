
A <-  c(
  -2,  -3, 1, 0, 0, 0,
  3, -1, 0, 1, 0, 0,
  -1, 1, 0, 0, 1, 0, 
  2, 5, 0, 0, 0, 1
)

A <- matrix(A, nrow = 4, byrow = T)
C <- c(2, 3, 0, 0, 0, 0)
b <- c(-6, 15, 4, 27)

x <- c(0, 0, -6, 15, 4, 27)

Cols <- seq_len(ncol(A))

B <- 3:6
N <- setdiff(Cols, B)

lambda <- solve(t(A[,B])) %*% C[B]
sn <- C[N] - t(A[,N])%*% lambda #for maximization: continue as long as max(sn) > 0

enter <- N[which.max(sn)]

d <- solve(A[,B]) %*% A[,enter]
ratios <- x[B]/d #get the ratios for the ratio test

multiplier <- min(ratios[d > 0]) #value of entering variable
exit <- B[which(ratios == multiplier)] 

x[enter] <- multiplier
x[B] <- x[B] - d*multiplier

B <- sort(union(setdiff(B, exit), enter))
N <- setdiff(Cols, B)

#repeat 39-54 until line 40 fails
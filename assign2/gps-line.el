(load "simple.el")

(defun count-newlines ()
  (save-excursion
    (beginning-of-buffer)
    (let ((count 0))
      (while (search-forward "\n" nil t)
	(setq count (1+ count)))
      (+ 0 count))))

(defun what-line ()
  "Print the current buffer line number and narrowed line number of point."
  (interactive)
  (let ((start (point-min))
        (n (line-number-at-pos)))
    (if (= start 1)
        (+ 0 n)
      ())))

(defun gps-line ()
  (interactive)
  (let ((line (what-line)))
    (let ((total (count-newlines)))
      (message "Line %d/%d" line total ))))
